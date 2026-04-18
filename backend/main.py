from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from celery_app import run_review, celery_app
import os

app = Flask(__name__)
CORS(app)

# -------------------------
# Existing Routes (unchanged)
# -------------------------

@app.route("/")
@cross_origin()
def home():
    return " Your backend is running :)"

@app.route("/test", methods=["GET"])
@cross_origin()
def test():
    return jsonify({
        "status": "success",
        "message": "Flask app is live and responding!"
    })

@app.route("/review", methods=["POST"])
@cross_origin()
def review():
    data = request.get_json()
    repo_url = data.get("repo_url")
    pr_number = data.get("pr_number")

    print(" Received review request for:", repo_url, "PR:", pr_number)

    if not repo_url:
        return jsonify({"error": "Missing repo URL"}), 400

    task = run_review.delay(repo_url, pr_number)

    return jsonify({
        "status": "queued",
        "task_id": task.id,
        "message": "Your PR review has been started in the background."
    }), 202

@app.route("/status/<task_id>", methods=["GET"])
@cross_origin()
def check_status(task_id):
    task = celery_app.AsyncResult(task_id)
    info = task.info if isinstance(task.info, dict) else {}

    print(f"[STATUS] Task {task_id} -> {task.state}, info: {info}")

    if task.state == "PENDING":
        response = {"status": "pending"}
    elif task.state == "PROGRESS":
        response = {
            "status": "in_progress",
            "message": info.get("message", "Working..."),
            "progress": info.get("progress", "0/0")
        }
    elif task.state == "SUCCESS":
        response = {
            "status": "completed",
            "message": info.get("message", "Review completed successfully."),
            "result": info.get("result")
        }
    elif task.state == "FAILURE":
        response = {
            "status": "failed",
            "message": str(task.info)
        }
    else:
        response = {
            "status": str(task.state),
            "message": info.get("message", "Review in progress...")
        }

    return jsonify(response)


# -------------------------
# ✅ Point 5 — Analytics Routes (Flask style)
# -------------------------

@app.route("/analytics/summary", methods=["GET"])
@cross_origin()
def analytics_summary():
    try:
        from analytics.models import SessionLocal, ReviewLog, create_tables
        from sqlalchemy import func
        create_tables()
        db = SessionLocal()

        total_reviews    = db.query(ReviewLog).count()
        total_violations = db.query(func.sum(ReviewLog.rule_violations)).scalar() or 0
        total_secrets    = db.query(func.sum(ReviewLog.secret_findings)).scalar() or 0
        total_owasp      = db.query(func.sum(ReviewLog.owasp_findings)).scalar() or 0
        critical_prs     = db.query(ReviewLog).filter(ReviewLog.has_critical == 1).count()
        db.close()

        return jsonify({
            "total_reviews": total_reviews,
            "total_rule_violations": int(total_violations),
            "total_secret_findings": int(total_secrets),
            "total_owasp_findings": int(total_owasp),
            "critical_prs": critical_prs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analytics/repos", methods=["GET"])
@cross_origin()
def analytics_repos():
    try:
        from analytics.models import SessionLocal, ReviewLog, create_tables
        from sqlalchemy import func
        create_tables()
        db = SessionLocal()

        results = db.query(
            ReviewLog.owner,
            ReviewLog.repo,
            func.count(ReviewLog.id).label("total_prs"),
            func.sum(ReviewLog.rule_violations).label("rule_violations"),
            func.sum(ReviewLog.secret_findings).label("secrets"),
            func.sum(ReviewLog.owasp_findings).label("owasp"),
            func.sum(ReviewLog.has_critical).label("critical_count")
        ).group_by(ReviewLog.owner, ReviewLog.repo).all()
        db.close()

        return jsonify([
            {
                "repo": f"{r.owner}/{r.repo}",
                "total_prs": r.total_prs,
                "rule_violations": int(r.rule_violations or 0),
                "secret_findings": int(r.secrets or 0),
                "owasp_findings": int(r.owasp or 0),
                "critical_prs": int(r.critical_count or 0)
            }
            for r in results
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analytics/recent", methods=["GET"])
@cross_origin()
def analytics_recent():
    try:
        from analytics.models import SessionLocal, ReviewLog, create_tables
        create_tables()
        db = SessionLocal()
        limit = request.args.get("limit", 10, type=int)

        reviews = db.query(ReviewLog).order_by(
            ReviewLog.created_at.desc()
        ).limit(limit).all()
        db.close()

        return jsonify([
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
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analytics/violations/top", methods=["GET"])
@cross_origin()
def analytics_top_violations():
    try:
        from analytics.models import SessionLocal, ViolationLog, create_tables
        from sqlalchemy import func
        create_tables()
        db = SessionLocal()
        limit = request.args.get("limit", 10, type=int)

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
        db.close()

        return jsonify([
            {
                "violation": r.name,
                "type": r.violation_type,
                "severity": r.severity,
                "occurrences": r.count
            }
            for r in results
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# from celery_app import run_review,celery_app  # import the task from celery_app.py
# import os


# app = Flask(__name__)
# CORS(app)  # enable global CORS

# @app.route("/")
# @cross_origin()
# def home():
#     return " Your backend is running :)"

# @app.route("/test", methods=["GET"])
# @cross_origin()
# def test():
#     return jsonify({
#         "status": "success",
#         "message": "Flask app is live and responding!"
#     })

# @app.route("/review", methods=["POST"])
# @cross_origin()  # CORS for frontend requests
# def review():
#     data = request.get_json()
#     repo_url = data.get("repo_url")
#     pr_number = data.get("pr_number")

#     print(" Received review request for:", repo_url, "PR:", pr_number)

#     if not repo_url:
#         return jsonify({"error": "Missing repo URL"}), 400

#     #  Queue the background task
#     task = run_review.delay(repo_url, pr_number)

#     return jsonify({
#         "status": "queued",
#         "task_id": task.id,
#         "message": "Your PR review has been started in the background."
#     }), 202

# @app.route("/status/<task_id>", methods=["GET"])
# @cross_origin()
# def check_status(task_id):
#     task = celery_app.AsyncResult(task_id)
#     info = task.info if isinstance(task.info, dict) else {}
    
#     print(f"[STATUS] Task {task_id} -> {task.state}, info: {info}")


#     if task.state == "PENDING":
#         response = {"status": "pending"}
#     elif task.state == "PROGRESS":
#         response = {
#             "status": "in_progress",
#             "message": info.get("message", "Working..."),
#             "progress": info.get("progress", "0/0")
#         }
#     elif task.state == "SUCCESS":
#         response = {
#             "status": "completed",
#             "message": info.get("message", "Review completed successfully."),
#             "result": info.get("result")
#         }
#     elif task.state == "FAILURE":
#         response = {
#             "status": "failed",
#             "message": str(task.info)
#         }
#     else:
#         response = {
#             "status": str(task.state),
#             "message": info.get("message", "Review in progress...")
#         }

#     return jsonify(response)



# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
