# config/rules_parser.py
import requests
import yaml
import re
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_rules_from_repo(owner, repo):
    """
    Repo ki .pr-review.yml file fetch karo GitHub se
    Agar file nahi hai to default rules return karo
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/.pr-review.yml"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 404:
            print("No .pr-review.yml found, using default rules")
            return get_default_rules()

        r.raise_for_status()
        import base64
        content = base64.b64decode(r.json()["content"]).decode("utf-8")
        rules = yaml.safe_load(content)
        return rules.get("rules", [])

    except Exception as e:
        print(f"Error fetching rules: {e}")
        return get_default_rules()


def get_default_rules():
    """Default rules jo har repo pe apply honge"""
    return [
        {
            "name": "No hardcoded passwords",
            "pattern": r"password\s*=\s*['\"].+['\"]",
            "severity": "critical",
            "message": "Hardcoded password detected! Use environment variables."
        },
        {
            "name": "No print statements in production",
            "pattern": r"\bprint\s*\(",
            "severity": "warning",
            "message": "Remove debug print statements before merging."
        },
        {
            "name": "No TODO comments",
            "pattern": r"#\s*TODO|//\s*TODO",
            "severity": "info",
            "message": "TODO comment found - make sure this is intentional."
        },
        {
            "name": "No commented out code blocks",
            "pattern": r"^[\+\-]\s*#.*\(|^[\+\-]\s*\/\/.*\(",
            "severity": "info",
            "message": "Commented-out code detected. Consider removing it."
        }
    ]


def check_rules_against_patch(patch, filename, rules):
    """
    Diff patch ke against rules check karo
    Sirf '+' lines check hongi (naya code)
    """
    violations = []

    # Sirf added lines lo (+ se start hone wali)
    added_lines = []
    for i, line in enumerate(patch.split("\n"), 1):
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append((i, line[1:]))  # line number, content

    for rule in rules:
        pattern = rule.get("pattern", "")
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
        except re.error:
            continue

        for line_num, line_content in added_lines:
            if compiled.search(line_content):
                violations.append({
                    "rule": rule["name"],
                    "severity": rule.get("severity", "warning"),
                    "message": rule.get("message", "Rule violation detected"),
                    "file": filename,
                    "line": line_num,
                    "matched_line": line_content.strip()
                })

    return violations


def format_violations_for_comment(violations):
    """Violations ko readable GitHub comment format mein convert karo"""
    if not violations:
        return ""

    severity_emoji = {
        "critical": "🔴",
        "high": "🟠",
        "warning": "🟡",
        "info": "🔵"
    }

    output = "### 📋 Custom Rule Violations\n\n"

    # Severity ke hisaab se group karo
    by_severity = {}
    for v in violations:
        sev = v["severity"]
        if sev not in by_severity:
            by_severity[sev] = []
        by_severity[sev].append(v)

    for severity in ["critical", "high", "warning", "info"]:
        if severity not in by_severity:
            continue
        emoji = severity_emoji.get(severity, "⚪")
        output += f"**{emoji} {severity.upper()}**\n"
        for v in by_severity[severity]:
            output += f"- `{v['file']}` → **{v['rule']}**: {v['message']}\n"
            output += f"  ```\n  {v['matched_line']}\n  ```\n"
        output += "\n"

    return output