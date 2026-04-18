# analytics/dashboard_api.py
from fastapi import APIRouter
from sqlalchemy import func
from analytics.models import SessionLocal, ReviewLog, ViolationLog, create_tables

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    create_tables()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_summary():
    """Overall stats — total reviews, violations, critical PRs"""
    db = SessionLocal()
    try:
        total_reviews = db.query(ReviewLog).count()
        total_violations = db.query(func.sum(ReviewLog.rule_violations)).scalar() or 0
        total_secrets = db.query(func.sum(ReviewLog.secret_findings)).scalar() or 0
        total_owasp = db.query(func.sum(ReviewLog.owasp_findings)).scalar() or 0
        critical_prs = db.query(ReviewLog).filter(ReviewLog.has_critical == 1).count()

        return {
            "total_reviews": total_reviews,
            "total_rule_violations": int(total_violations),
            "total_secret_findings": int(total_secrets),
            "total_owasp_findings": int(total_owasp),
            "critical_prs": critical_prs
        }
    finally:
        db.close()


@router.get("/repos")
def get_repo_stats():
    """Repo-wise breakdown"""
    db = SessionLocal()
    try:
        results = db.query(
            ReviewLog.owner,
            ReviewLog.repo,
            func.count(ReviewLog.id).label("total_prs"),
            func.sum(ReviewLog.rule_violations).label("rule_violations"),
            func.sum(ReviewLog.secret_findings).label("secrets"),
            func.sum(ReviewLog.owasp_findings).label("owasp"),
            func.sum(ReviewLog.has_critical).label("critical_count")
        ).group_by(ReviewLog.owner, ReviewLog.repo).all()

        return [
            {
                "repo": f"{r.owner}/{r.repo}",
                "total_prs": r.total_prs,
                "rule_violations": int(r.rule_violations or 0),
                "secret_findings": int(r.secrets or 0),
                "owasp_findings": int(r.owasp or 0),
                "critical_prs": int(r.critical_count or 0)
            }
            for r in results
        ]
    finally:
        db.close()


@router.get("/recent")
def get_recent_reviews(limit: int = 10):
    """Last N reviews"""
    db = SessionLocal()
    try:
        reviews = db.query(ReviewLog).order_by(
            ReviewLog.created_at.desc()
        ).limit(limit).all()

        return [
            {
                "id": r.id,
                "repo": f"{r.owner}/{r.repo}",
                "pr_number": r.pr_number,
                "files_reviewed": r.files_reviewed,
                "rule_violations": r.rule_violations,
                "secret_findings": r.secret_findings,
                "owasp_findings": r.owasp_findings,
                "has_critical": bool(r.has_critical),
                "reviewed_at": r.created_at.isoformat()
            }
            for r in reviews
        ]
    finally:
        db.close()


@router.get("/violations/top")
def get_top_violations(limit: int = 10):
    """Sabse common violations"""
    db = SessionLocal()
    try:
        results = db.query(
            ViolationLog.name,
            ViolationLog.violation_type,
            ViolationLog.severity,
            func.count(ViolationLog.id).label("count")
        ).group_by(
            ViolationLog.name,
            ViolationLog.violation_type,
            ViolationLog.severity
        ).order_by(func.count(ViolationLog.id).desc()).limit(limit).all()

        return [
            {
                "violation": r.name,
                "type": r.violation_type,
                "severity": r.severity,
                "occurrences": r.count
            }
            for r in results
        ]
    finally:
        db.close()