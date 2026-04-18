# security/secret_scanner.py
import re

# Common secret patterns
SECRET_PATTERNS = [
    {
        "name": "AWS Access Key",
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "critical"
    },
    {
        "name": "AWS Secret Key",
        "pattern": r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]",
        "severity": "critical"
    },
    {
        "name": "Google API Key",
        "pattern": r"AIza[0-9A-Za-z\-_]{35}",
        "severity": "critical"
    },
    {
        "name": "GitHub Token",
        "pattern": r"gh[pousr]_[0-9a-zA-Z]{36}",
        "severity": "critical"
    },
    {
        "name": "JWT Token",
        "pattern": r"eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_.+/=]*",
        "severity": "high"
    },
    {
        "name": "Private Key Block",
        "pattern": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        "severity": "critical"
    },
    {
        "name": "Hardcoded Password",
        "pattern": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{4,}['\"]",
        "severity": "critical"
    },
    {
        "name": "Hardcoded Secret",
        "pattern": r"(?i)(secret|api_key|apikey|auth_token)\s*=\s*['\"][^'\"]{4,}['\"]",
        "severity": "critical"
    },
    {
        "name": "Stripe API Key",
        "pattern": r"sk_live_[0-9a-zA-Z]{24}",
        "severity": "critical"
    },
    {
        "name": "Slack Token",
        "pattern": r"xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9a-zA-Z]{24}",
        "severity": "high"
    }
]


def scan_for_secrets(patch, filename):
    """
    Patch mein secrets scan karo
    Sirf added lines (+) check hongi
    """
    findings = []

    added_lines = []
    for i, line in enumerate(patch.split("\n"), 1):
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append((i, line[1:]))

    for pattern_info in SECRET_PATTERNS:
        try:
            compiled = re.compile(pattern_info["pattern"])
        except re.error:
            continue

        for line_num, line_content in added_lines:
            if compiled.search(line_content):
                # Actual value mask karo log mein
                masked = re.sub(pattern_info["pattern"], "***REDACTED***", line_content)
                findings.append({
                    "type": pattern_info["name"],
                    "severity": pattern_info["severity"],
                    "file": filename,
                    "line": line_num,
                    "masked_content": masked.strip()
                })

    return findings


def format_secret_findings(findings):
    """Secret findings ko GitHub comment format mein convert karo"""
    if not findings:
        return ""

    output = "### 🔐 Secret / Credential Detection\n\n"
    output += "> ⚠️ **CRITICAL: Potential secrets detected! Do NOT merge this PR.**\n\n"

    for f in findings:
        output += f"- 🔴 **{f['type']}** found in `{f['file']}` (line ~{f['line']})\n"
        output += f"  ```\n  {f['masked_content']}\n  ```\n"

    output += "\n**Action Required:** Remove secrets and use environment variables instead.\n"
    return output