# github_app/check_runs.py
import requests
import os
from datetime import datetime, timezone
from github_app.app_auth import get_token_for_repo

def create_check_run(owner, repo, head_sha, has_critical,
                     rule_violations, secret_findings, owasp_findings):
    """
    GitHub Check Run create karo — PR pe inline status dikhega
    (Comments se better — official pass/fail status)
    """
    try:
        token = get_token_for_repo(owner, repo)
    except Exception as e:
        print(f"GitHub App token fetch failed, skipping check run: {e}")
        return

    total_issues = len(rule_violations) + len(secret_findings) + len(owasp_findings)

    # Pass ya fail decide karo
    conclusion = "failure" if has_critical else ("warning" if total_issues > 0 else "success")

    # Summary banao
    summary_lines = [
        f"**Files Reviewed:** (see comment)",
        f"**Rule Violations:** {len(rule_violations)}",
        f"**Secrets Found:** {len(secret_findings)}",
        f"**OWASP Issues:** {len(owasp_findings)}",
    ]

    if has_critical:
        summary_lines.append("\n🔴 **Critical issues found — merge blocked!**")
    elif total_issues == 0:
        summary_lines.append("\n✅ **All checks passed!**")
    else:
        summary_lines.append(f"\n⚠️ **{total_issues} issue(s) found — review before merging.**")

    # Annotations banao (inline PR comments — file level)
    annotations = []

    for f in secret_findings[:10]:  # Max 10 annotations
        annotations.append({
            "path": f.get("file", "unknown"),
            "start_line": f.get("line", 1),
            "end_line": f.get("line", 1),
            "annotation_level": "failure",
            "title": f"🔴 Secret Detected: {f.get('type')}",
            "message": "A potential secret/credential was found. Remove and use env vars."
        })

    for f in owasp_findings[:10]:
        level = "failure" if f["severity"] == "critical" else "warning"
        annotations.append({
            "path": f.get("file", "unknown"),
            "start_line": f.get("line", 1),
            "end_line": f.get("line", 1),
            "annotation_level": level,
            "title": f"🛡️ {f.get('name')}",
            "message": f.get("message", "")
        })

    url = f"https://api.github.com/repos/{owner}/{repo}/check-runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "name": "RevAI Security Review",
        "head_sha": head_sha,
        "status": "completed",
        "conclusion": conclusion,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "output": {
            "title": f"RevAI: {total_issues} issue(s) found",
            "summary": "\n".join(summary_lines),
            "annotations": annotations[:50]  # GitHub max 50 annotations per run
        }
    }

    r = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Check Run Status: {r.status_code}")
    r.raise_for_status()