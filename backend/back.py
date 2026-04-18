from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time

#Added claude
from config.rules_parser import fetch_rules_from_repo, check_rules_against_patch, format_violations_for_comment
from security.secret_scanner import scan_for_secrets, format_secret_findings
from security.owasp_scanner import scan_owasp, format_owasp_findings, has_critical_findings
from analytics.logger import log_review


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    max_retries=0,
)

SUPPORTED_EXTENSIONS = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".jsx": Language.JS,
    ".ts": Language.TS,
    ".tsx": Language.TS,
    ".java": Language.JAVA,
    ".cpp": Language.CPP
}

SKIP_PATHS = [
    "node_modules",
    "dist",
    "build",
    ".git",
    "__pycache__",
    "coverage"
]


def get_extension(filename):
    return os.path.splitext(filename)[1]


# -------------------------
# Fetch PR Changed Files
# -------------------------

def fetch_pr_files(owner, repo, pr_number):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 403:
        raise Exception("GitHub Rate Limit Hit")
    r.raise_for_status()

    files = r.json()
    code_files = []

    for f in files:
        filename = f["filename"]

        if any(skip in filename for skip in SKIP_PATHS):
            continue

        ext = get_extension(filename)
        if ext not in SUPPORTED_EXTENSIONS:
            continue

        patch = f.get("patch")
        if not patch:
            continue

        status = f.get("status")  # "added", "modified", "removed"

        # ✅ Nayi file hai to full content fetch karo
        if status == "added":
            full_content = fetch_full_file_content(owner, repo, filename)
            code_files.append({
                "name": os.path.basename(filename),
                "path": filename,
                "patch": patch,
                "full_content": full_content,  # puri file
                "is_new_file": True
            })
        else:
            code_files.append({
                "name": os.path.basename(filename),
                "path": filename,
                "patch": patch,
                "full_content": None,
                "is_new_file": False
            })

    print(f"Found {len(code_files)} changed code files")
    return code_files


def fetch_full_file_content(owner, repo, filepath):
    """Nayi file ka pura content fetch karo"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        import base64
        content = base64.b64decode(r.json()["content"]).decode("utf-8")
        return content
    except Exception as e:
        print(f"Could not fetch full content for {filepath}: {e}")
        return None
    
# def fetch_pr_files(owner, repo, pr_number):

#     url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

#     headers = {
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github+json"
#     }

#     r = requests.get(url, headers=headers, timeout=10)

#     if r.status_code == 403:
#         raise Exception("GitHub Rate Limit Hit")

#     r.raise_for_status()

#     files = r.json()

#     code_files = []

#     for f in files:

#         filename = f["filename"]

#         if any(skip in filename for skip in SKIP_PATHS):
#             continue

#         ext = get_extension(filename)

#         if ext in SUPPORTED_EXTENSIONS:

#             patch = f.get("patch")

#             if not patch:
#                 continue

#             code_files.append({
#                 "name": os.path.basename(filename),
#                 "path": filename,
#                 "patch": patch
#             })

#     print(f"Found {len(code_files)} changed code files")

#     return code_files

# -------------------------
# Language Aware Splitter
# -------------------------

def split_code(content, filename):

    ext = get_extension(filename)

    if ext in SUPPORTED_EXTENSIONS:

        splitter = RecursiveCharacterTextSplitter.from_language(
            language=SUPPORTED_EXTENSIONS[ext],
            chunk_size=1000,
            chunk_overlap=200
        )

    else:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    return splitter.split_text(content)


# -------------------------
# Prompt
# -------------------------
code_review_prompt = PromptTemplate(
template="""
You are a senior software engineer reviewing a GitHub pull request.

File: {filename}

{context_note}

Code:
{code}

Focus on:
- logical errors
- performance issues
- edge cases
- security concerns

Respond with MAX 5 concise bullet points.
If code looks good respond with a short positive note.
""",
input_variables=["filename", "code", "context_note"]
)


# -------------------------
# Review File
# -------------------------

def review_file(file):
    patch = file["patch"]
    is_new = file.get("is_new_file", False)
    full_content = file.get("full_content")

    # Nayi file hai aur full content available hai
    if is_new and full_content:
        code_to_review = full_content
        context_note = "This is a NEW file added in this PR. Review the entire file."
    else:
        code_to_review = patch
        context_note = "Only analyze the CHANGED lines."

    if len(code_to_review) > 8000:
        print("Skipping very large diff")
        return None

    prompt = code_review_prompt.format(
        filename=file["name"],
        code=code_to_review,
        context_note=context_note  # ← prompt mein add karo
    )

    response = model.invoke(prompt)
    return {
        "file": file["name"],
        "review": response.content
    }


# -------------------------
# Post PR Comment
# -------------------------

def post_pr_comment(owner, repo, pr_number, body):

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.post(
        url,
        headers=headers,
        json={"body": body},
        timeout=10
    )

    print("GitHub Response:", r.status_code)

    r.raise_for_status()


# -------------------------
# Review Repo PR
# -------------------------

# def review_repo(owner, repo, pr_number):

#     files = fetch_pr_files(owner, repo, pr_number)

#     reviews = []

#     with ThreadPoolExecutor(max_workers=4) as executor:

#         results = executor.map(review_file, files)

#     for r in results:

#         if r:
#             reviews.append(r)

#     combined_review = "# 🤖 AI Code Review\n\n"

#     for r in reviews:

#         combined_review += f"## {r['file']}\n"
#         combined_review += r["review"]
#         combined_review += "\n\n"

#     post_pr_comment(owner, repo, pr_number, combined_review)

#     return reviews

def review_repo(owner, repo, pr_number, head_sha=None):

    files = fetch_pr_files(owner, repo, pr_number)

    # Point 3: Custom rules fetch karo
    rules = fetch_rules_from_repo(owner, repo)

    reviews = []
    all_rule_violations = []
    all_secret_findings = []
    all_owasp_findings = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(review_file, files))

    for i, r in enumerate(results):
        if r:
            reviews.append(r)
            # ✅ Nayi file ke liye full content, modified ke liye patch
            file_obj = files[i]
            scan_content = file_obj.get("full_content") or file_obj["patch"]
            fname = file_obj["path"]
            
            # Point 3: Rules check
            violations = check_rules_against_patch(scan_content, fname, rules)
            all_rule_violations.extend(violations)

            # Point 4: Security scan
            secrets = scan_for_secrets(scan_content, fname)
            owasp = scan_owasp(scan_content, fname)

            all_secret_findings.extend(secrets)
            all_owasp_findings.extend(owasp)
            
            # print(f"DEBUG FILE: {fname}")
            # print(f"DEBUG VIOLATIONS: {violations}")
            # print(f"DEBUG SECRETS: {secrets}")
            # print(f"DEBUG OWASP: {owasp}")

    # Comment build karo
    combined_review = "# 🤖 RevAI Code Review\n\n"

    # Security section pehle (critical hoga to upar dikhega)
    combined_review += format_secret_findings(all_secret_findings)
    combined_review += format_owasp_findings(all_owasp_findings)
    combined_review += format_violations_for_comment(all_rule_violations)

    # AI Review
    combined_review += "---\n### 🧠 AI Review\n\n"
    for r in reviews:
        combined_review += f"## {r['file']}\n"
        combined_review += r["review"]
        combined_review += "\n\n"

    post_pr_comment(owner, repo, pr_number, combined_review)

    # Point 5: Analytics log karo
    is_critical = has_critical_findings(all_owasp_findings, all_secret_findings)
    log_review(
        owner=owner, repo=repo, pr_number=pr_number,
        files_reviewed=len(files),
        rule_violations=all_rule_violations,
        secret_findings=all_secret_findings,
        owasp_findings=all_owasp_findings,
        has_critical=is_critical,
        review_data=reviews
    )

    # Point 10: GitHub Check Run (only if head_sha available)
    if head_sha:
        from github_app.check_runs import create_check_run
        create_check_run(
            owner, repo, head_sha, is_critical,
            all_rule_violations, all_secret_findings, all_owasp_findings
        )

    return reviews


# -------------------------
# Get Latest PR
# -------------------------

def get_latest_pr(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&sort=created&direction=desc"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    r = requests.get(url, headers=headers, timeout=10)

    r.raise_for_status()

    prs = r.json()

    if not prs:
        return None

    return prs[0]["number"]


# -------------------------
# Main Entry
# -------------------------

def review_repository(repo_url, pr_number=None):

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    if not pr_number:
        pr_number = get_latest_pr(owner, repo)

    if not pr_number:
        return {"error": "No open PR found"}

    print("Reviewing PR:", pr_number)

    return review_repo(owner, repo, pr_number)




# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.prompts import PromptTemplate
# from concurrent.futures import ThreadPoolExecutor
# import requests
# import time
# import os

# load_dotenv()

# model = ChatGoogleGenerativeAI(
#     model='gemini-2.5-flash',
#     max_retries=0,
# )

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# # def fetch_repo_content(owner, repo_name, path=""):
# #     url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
# #     headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
# #     response = requests.get(url, headers=headers)
# #     response.raise_for_status()
# #     return response.json()

# def fetch_all_files(owner, repo_name):
#     """
#     Fetch all code files (.py, .js, .jsx, .ts, .tsx, .java, .cpp) from a GitHub repo,
#     including nested directories, using the correct default branch.
#     """
#     headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

#     # Step 1: Detect default branch
#     repo_info_url = f"https://api.github.com/repos/{owner}/{repo_name}"
#     repo_info_resp = requests.get(repo_info_url, headers=headers)
#     repo_info_resp.raise_for_status()
#     default_branch = repo_info_resp.json().get("default_branch", "main")

#     # Step 2: Fetch the full tree recursively
#     tree_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/{default_branch}?recursive=1"
#     tree_resp = requests.get(tree_url, headers=headers)
#     tree_resp.raise_for_status()
#     tree_data = tree_resp.json().get("tree", [])

#     files = []
#     for item in tree_data:
#         if (
#             item["type"] == "blob"
#             and item["path"].endswith((".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp"))
#         ):
#             download_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{default_branch}/{item['path']}"
#             files.append({
#                 "name": os.path.basename(item["path"]),
#                 "path": item["path"],
#                 "download_url": download_url,
#                 "type": "file"
#             })

#     print(f"[INFO] Found {len(files)} code files in branch '{default_branch}'")
#     return files


# def download_url(file_info):
#     if file_info["type"] == 'file':
#         size = file_info.get("size", 0)  # Default to 0 if size not present
#         if size and size > 100_000:  # Skip only if size is known and large
#             print(f"Skipping large file: {file_info['name']}")
#             return None

#         url = file_info["download_url"]
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.text
#     return None


# import os

# # def get_all_code_files(repo_path, exts=(".py", ".js", ".java", ".cpp", ".ts")):
# #     code_files = []
# #     for root, _, files in os.walk(repo_path):
# #         if any(skip in root for skip in ['node_modules', '.git', '__pycache__']):
# #             continue
# #         for file in files:
# #             if file.endswith(exts):
# #                 code_files.append(os.path.join(root, file))
# #     return code_files


# def code_splitter(code, chunk_size=500, chunk_overlap=50):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n"]
#     )
#     doc = Document(page_content=code)
#     return splitter.split_text(doc.page_content)

# code_review_prompt = PromptTemplate(
#     template="""
#            You are a senior code reviewer.

#            Review this code snippet from file `{filename}`:

#            {code}

#            Give short, **point-to-point** feedback in bullet format.
#            - Focus ONLY on logic, readability, and performance.
#            - Do NOT mention naming or formatting unless it's seriously wrong.
#            - Max 5 concise points.
#            - If the code is clean, respond with 1 or 2 encouraging lines only.
#              """,
#     input_variables=["filename", "code"]
# )


# def process_file(file):
#     # Skip irrelevant files
#     skip_files = {
#         "vite.config.js", "eslint.config.js", "tailwind.config.js",
#         "package-lock.json", "yarn.lock", "package.json",
#         "README.md", "postcss.config.js"
#     }

#     if file["name"] in skip_files or file["name"].endswith((".json", ".lock")):
#         print(f"Skipping irrelevant file: {file['name']}")
#         return None

#     content = download_url(file)
#     if not content:
#         return None

#     # Only review supported code types
#     if not file["name"].endswith((".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp")):
#         print(f"Skipping unsupported file type: {file['name']}")
#         return None

#     chunks = [c for c in code_splitter(content) if c.strip()]
#     reviews = []
#     for chunk in chunks:
#         formatted_prompt = code_review_prompt.format(filename=file["name"], code=chunk)
#         review = model.invoke(formatted_prompt)
#         reviews.append(review.content)
#         time.sleep(0.3)  # small pause between Gemini calls

#     return {"file": file["name"], "review": "\n".join(reviews)}


# def review_repo(owner, repo_name,pr_number=None):
#     files = fetch_all_files(owner, repo_name)
#     all_reviews = []

#     with ThreadPoolExecutor(max_workers=1) as executor:
#         results = executor.map(process_file, files)

#     for res in results:
#         if res:
#             all_reviews.append(res)
#             print(f"Reviewed {res['file']}")
#             # Post comment immediately for each file
#             if pr_number:
#                 comment_body = f"### Review for `{res['file']}`\n{res['review']}"
#                 post_pr_comment(owner, repo_name, pr_number, comment_body, GITHUB_TOKEN)
#     return all_reviews


# def post_pr_comment(owner, repo, pr_number, body, token):
#     import requests
    
#     print("function which adds Comments on github reached")
#     url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
#     headers = {
#         "Authorization": f"Bearer {token}",  #  use Bearer instead of 'token'
#         "Accept": "application/vnd.github+json"
#     }
#     data = {"body": body}

#     r = requests.post(url, headers=headers, json=data)
#     print("GitHub API response:", r.status_code, r.text)  # 👀 See what GitHub says

#     if r.status_code == 201:
#         print(f"Comment posted on PR #{pr_number}")
#     else:
#         print(f"Failed to post comment on PR #{pr_number}")
#     return r


# def get_latest_pr_number(owner, repo):
#     """Fetches the latest open pull request number."""
#     url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&sort=created&direction=desc"
#     headers = {
#         "Authorization": f"Bearer {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github+json"
#     }
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     prs = response.json()
#     if prs:
#         latest_pr = prs[0]
#         print(f"Latest PR found: #{latest_pr['number']}")
#         return latest_pr["number"]
#     print(" No open PRs found.")
#     return None


# def review_repository(repo_url,pr_number=None):
#     try:
#         parts = repo_url.rstrip("/").split("/")
#         owner, repo = parts[-2], parts[-1]
        
#         if not pr_number:
#             pr_number = get_latest_pr_number(owner, repo)

#         print("PR number being used for review:", pr_number)

#         # print(f"Reviewing repository: {owner}/{repo}...")
#         result = review_repo(owner, repo,pr_number)
#         return result
#     except Exception as e:
#         return {"error": str(e)}
