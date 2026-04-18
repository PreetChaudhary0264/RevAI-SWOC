# github_app/app_auth.py
import jwt
import time
import requests
import os

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_APP_PRIVATE_KEY = os.getenv("GITHUB_APP_PRIVATE_KEY", "").replace("\\n", "\n")


def generate_jwt():
    """
    GitHub App JWT token generate karo
    Ye har API call se pehle chahiye
    """
    now = int(time.time())
    payload = {
        "iat": now - 60,       # issued at (60s pehle for clock skew)
        "exp": now + 600,       # expires in 10 min
        "iss": GITHUB_APP_ID
    }

    token = jwt.encode(payload, GITHUB_APP_PRIVATE_KEY, algorithm="RS256")
    return token


def get_installation_token(installation_id):
    """
    Installation-specific access token lo
    Har repo install ke liye alag token hota hai
    """
    jwt_token = generate_jwt()

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.post(url, headers=headers, timeout=10)
    r.raise_for_status()

    return r.json()["token"]


def get_installation_id(owner, repo):
    """
    Repo ke liye installation ID fetch karo
    """
    jwt_token = generate_jwt()

    url = f"https://api.github.com/repos/{owner}/{repo}/installation"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    return r.json()["id"]


def get_token_for_repo(owner, repo):
    """
    Ek function se seedha repo ka token lo
    back.py mein GITHUB_TOKEN ki jagah ye use karo
    """
    installation_id = get_installation_id(owner, repo)
    return get_installation_token(installation_id)