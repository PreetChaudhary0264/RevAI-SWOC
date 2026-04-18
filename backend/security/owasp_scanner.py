# security/owasp_scanner.py
import re

# OWASP Top 10 patterns
OWASP_PATTERNS = [
    # A1 - Injection
    {
        "name": "SQL Injection Risk",
        "pattern": r"(?i)(execute|query|cursor\.execute)\s*\(\s*[f'\"].*\{|\".*\+.*(?:user|input|param|request)",
        "category": "A1-Injection",
        "severity": "critical",
        "message": "Possible SQL injection. Use parameterized queries instead."
    },
    {
        "name": "OS Command Injection",
        "pattern": r"(?i)(os\.system|subprocess\.call|subprocess\.run|eval|exec)\s*\(.*\+",
        "category": "A1-Injection",
        "severity": "critical",
        "message": "Possible command injection. Never pass user input to system commands."
    },
    # A2 - Broken Auth
    {
        "name": "Weak Hashing Algorithm",
        "pattern": r"(?i)(md5|sha1)\s*\(",
        "category": "A2-Broken-Auth",
        "severity": "high",
        "message": "MD5/SHA1 are weak for password hashing. Use bcrypt or argon2."
    },
    # A3 - XSS
    {
        "name": "XSS Risk - innerHTML",
        "pattern": r"innerHTML\s*=",
        "category": "A3-XSS",
        "severity": "high",
        "message": "innerHTML can lead to XSS. Use textContent or sanitize input."
    },
    {
        "name": "XSS Risk - dangerouslySetInnerHTML",
        "pattern": r"dangerouslySetInnerHTML",
        "category": "A3-XSS",
        "severity": "high",
        "message": "dangerouslySetInnerHTML detected. Ensure content is sanitized."
    },
    # A5 - Security Misconfiguration
    {
        "name": "Debug Mode Enabled",
        "pattern": r"(?i)(DEBUG\s*=\s*True|app\.run\(.*debug\s*=\s*True)",
        "category": "A5-Misconfiguration",
        "severity": "high",
        "message": "Debug mode should never be enabled in production."
    },
    {
        "name": "CORS Wildcard",
        "pattern": r"(?i)(Access-Control-Allow-Origin.*\*|allow_origins.*\[.*\*.*\])",
        "category": "A5-Misconfiguration",
        "severity": "high",
        "message": "Wildcard CORS policy is insecure. Specify allowed origins explicitly."
    },
    # A8 - Insecure Deserialization
    {
        "name": "Unsafe Pickle Usage",
        "pattern": r"pickle\.loads?\s*\(",
        "category": "A8-Deserialization",
        "severity": "critical",
        "message": "pickle.load with untrusted data can lead to RCE. Use JSON instead."
    },
    # A9 - Vulnerable Components
    {
        "name": "Dangerous eval()",
        "pattern": r"\beval\s*\(",
        "category": "A1-Injection",
        "severity": "critical",
        "message": "eval() with user input is extremely dangerous. Avoid it entirely."
    },
    # Generic
    {
        "name": "Unvalidated Redirect",
        "pattern": r"(?i)redirect\s*\(\s*(request\.|user_input|params)",
        "category": "A10-Redirects",
        "severity": "medium",
        "message": "Unvalidated redirect detected. Validate destination URL."
    }
]


def scan_owasp(patch, filename):
    """OWASP vulnerabilities scan karo diff mein"""
    findings = []

    added_lines = []
    for i, line in enumerate(patch.split("\n"), 1):
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append((i, line[1:]))

    for pattern_info in OWASP_PATTERNS:
        try:
            compiled = re.compile(pattern_info["pattern"])
        except re.error:
            continue

        for line_num, line_content in added_lines:
            if compiled.search(line_content):
                findings.append({
                    "name": pattern_info["name"],
                    "category": pattern_info["category"],
                    "severity": pattern_info["severity"],
                    "message": pattern_info["message"],
                    "file": filename,
                    "line": line_num,
                    "code": line_content.strip()
                })

    return findings


def format_owasp_findings(findings):
    """OWASP findings ko GitHub comment format mein convert karo"""
    if not findings:
        return ""

    severity_emoji = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🔵"
    }

    output = "### 🛡️ Security Vulnerabilities (OWASP)\n\n"

    for f in findings:
        emoji = severity_emoji.get(f["severity"], "⚪")
        output += f"- {emoji} **{f['name']}** `[{f['category']}]` in `{f['file']}` (line ~{f['line']})\n"
        output += f"  - _{f['message']}_\n"
        output += f"  ```\n  {f['code']}\n  ```\n"

    return output


def has_critical_findings(owasp_findings, secret_findings):
    """Check karo koi critical issue hai ya nahi (PR block karne ke liye)"""
    for f in owasp_findings:
        if f["severity"] == "critical":
            return True
    for f in secret_findings:
        if f["severity"] == "critical":
            return True
    return False