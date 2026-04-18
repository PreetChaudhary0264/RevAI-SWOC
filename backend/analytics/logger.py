# analytics/logger.py
from analytics.models import SessionLocal, ReviewLog, ViolationLog, create_tables


def log_review(owner, repo, pr_number, files_reviewed,
               rule_violations, secret_findings,
               owasp_findings, has_critical, review_data=None):
    """PR review ka summary database mein save karo"""

    create_tables()  # Tables exist nahi hai to create karo
    db = SessionLocal()

    try:
        log = ReviewLog(
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            files_reviewed=files_reviewed,
            rule_violations=len(rule_violations),
            secret_findings=len(secret_findings),
            owasp_findings=len(owasp_findings),
            has_critical=1 if has_critical else 0,
            review_data=review_data
        )
        db.add(log)

        # Individual violations bhi log karo
        for v in rule_violations:
            db.add(ViolationLog(
                owner=owner, repo=repo, pr_number=pr_number,
                violation_type="rule",
                severity=v.get("severity", "warning"),
                name=v.get("rule", ""),
                file=v.get("file", ""),
                message=v.get("message", "")
            ))

        for v in secret_findings:
            db.add(ViolationLog(
                owner=owner, repo=repo, pr_number=pr_number,
                violation_type="secret",
                severity=v.get("severity", "critical"),
                name=v.get("type", ""),
                file=v.get("file", ""),
                message=f"Secret detected: {v.get('type')}"
            ))

        for v in owasp_findings:
            db.add(ViolationLog(
                owner=owner, repo=repo, pr_number=pr_number,
                violation_type="owasp",
                severity=v.get("severity", "high"),
                name=v.get("name", ""),
                file=v.get("file", ""),
                message=v.get("message", "")
            ))

        db.commit()
        print(f"✅ Analytics logged for PR #{pr_number}")

    except Exception as e:
        print(f"❌ Analytics logging failed: {e}")
        db.rollback()
    finally:
        db.close()