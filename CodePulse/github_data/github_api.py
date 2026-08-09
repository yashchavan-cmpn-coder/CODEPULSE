import os

import requests
from dotenv import load_dotenv

from .models import (
    Repository,
    Commit,
    PullRequest,
    Issue,
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# GITHUB API CONFIGURATION
# =========================================================

GITHUB_API_URL = "https://api.github.com"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = (
        f"Bearer {GITHUB_TOKEN}"
    )


# =========================================================
# GITHUB API REQUEST
# =========================================================

def github_request(url, params=None):
    """
    Send an authenticated request to GitHub.

    Provides:
    - Environment-based token authentication
    - Request timeout
    - Rate-limit handling
    - Authentication error handling
    - Network error handling
    """

    # -----------------------------------------------------
    # Check GitHub token
    # -----------------------------------------------------

    if not GITHUB_TOKEN:
        print(
            "GitHub token is not configured."
        )
        return None

    # -----------------------------------------------------
    # Send request
    # -----------------------------------------------------

    try:

        response = requests.get(
            url,
            headers=GITHUB_HEADERS,
            params=params,
            timeout=15,
        )

    except requests.RequestException as error:

        print(
            "GitHub API request failed:",
            error,
        )

        return None

    # -----------------------------------------------------
    # Successful response
    # -----------------------------------------------------

    if response.status_code == 200:
        return response.json()

    # -----------------------------------------------------
    # Authentication failure
    # -----------------------------------------------------

    if response.status_code == 401:

        print(
            "GitHub authentication failed."
        )

        print(
            "Check GITHUB_TOKEN in the .env file."
        )

        return None

    # -----------------------------------------------------
    # Rate limit / access denied
    # -----------------------------------------------------

    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        reset_time = response.headers.get(
            "X-RateLimit-Reset"
        )

        print(
            "GitHub API access denied "
            "or rate limit exceeded."
        )

        print(
            "Remaining requests:",
            remaining,
        )

        print(
            "Rate limit reset timestamp:",
            reset_time,
        )

        return None

    # -----------------------------------------------------
    # Other API errors
    # -----------------------------------------------------

    print(
        "GitHub API request failed:",
        response.status_code,
        response.text,
    )

    return None


# =========================================================
# GITHUB USER
# =========================================================

def get_github_user(username):

    url = (
        f"{GITHUB_API_URL}/users/{username}"
    )

    return github_request(url)


# =========================================================
# GITHUB REPOSITORIES
# =========================================================

def get_github_repositories(username):

    repositories = []

    page = 1

    while True:

        url = (
            f"{GITHUB_API_URL}/users/"
            f"{username}/repos"
        )

        params = {
            "page": page,
            "per_page": 100,
            "type": "all",
            "sort": "updated",
        }

        page_repositories = github_request(
            url,
            params=params,
        )

        if page_repositories is None:
            break

        if not page_repositories:
            break

        repositories.extend(
            page_repositories
        )

        if len(page_repositories) < 100:
            break

        page += 1

    return repositories


# =========================================================
# SYNC REPOSITORIES
# =========================================================

def sync_repositories(developer_profile):

    repositories = get_github_repositories(
        developer_profile.github_username
    )

    if not repositories:
        return

    for repo in repositories:

        Repository.objects.update_or_create(

            github_id=repo["id"],

            defaults={

                "developer":
                    developer_profile,

                "name":
                    repo["name"],

                "full_name":
                    repo["full_name"],

                "description":
                    repo["description"] or "",

                "html_url":
                    repo["html_url"],

                "language":
                    repo["language"] or "",

                "stars":
                    repo["stargazers_count"],

                "forks":
                    repo["forks_count"],

                "is_fork":
                    repo["fork"],

                "created_at":
                    repo["created_at"],

                "updated_at":
                    repo["updated_at"],

                "pushed_at":
                    repo["pushed_at"],
            }
        )


# =========================================================
# GITHUB COMMITS
# =========================================================

def get_github_commits(owner, repo):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/commits"
    )

    response = github_request(url)

    return response or []


# =========================================================
# SYNC COMMITS
# =========================================================

def sync_commits(repository):

    owner = (
        repository.full_name.split("/")[0]
    )

    repo_name = repository.name

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo_name}/commits"
    )

    try:

        response = requests.get(
            url,
            headers=GITHUB_HEADERS,
            timeout=15,
        )

    except requests.RequestException as error:

        print(
            "GitHub commit request failed:",
            error,
        )

        return

    # -----------------------------------------------------
    # Empty repository
    # -----------------------------------------------------

    if response.status_code == 409:

        print(
            f"Repository '{owner}/{repo_name}' "
            "is empty. No commits to sync."
        )

        return

    # -----------------------------------------------------
    # Other errors
    # -----------------------------------------------------

    if response.status_code != 200:

        print(
            "GitHub commit request failed:",
            response.status_code,
        )

        return

    commits = response.json()

    # -----------------------------------------------------
    # Save commits
    # -----------------------------------------------------

    for commit_data in commits:

        commit_info = (
            commit_data["commit"]
        )

        author = (
            commit_info.get("author")
            or {}
        )

        Commit.objects.update_or_create(

            github_sha=commit_data["sha"],

            defaults={

                "repository":
                    repository,

                "message":
                    commit_info.get(
                        "message",
                        "",
                    ),

                "author_name":
                    author.get(
                        "name",
                        "",
                    ),

                "author_email":
                    author.get(
                        "email",
                        "",
                    ),

                "committed_at":
                    author.get(
                        "date"
                    ),

                "html_url":
                    commit_data.get(
                        "html_url",
                        "",
                    ),
            }
        )


# =========================================================
# GITHUB PULL REQUESTS
# =========================================================

def get_github_pull_requests(
    owner,
    repo,
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/pulls"
    )

    params = {
        "state": "all",
    }

    response = github_request(
        url,
        params=params,
    )

    return response or []


# =========================================================
# GITHUB ISSUES
# =========================================================

def get_github_issues(
    owner,
    repo,
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/issues"
    )

    params = {
        "state": "all",
    }

    response = github_request(
        url,
        params=params,
    )

    return response or []


# =========================================================
# SYNC PULL REQUESTS
# =========================================================

def sync_pull_requests(repository):

    owner = (
        repository.full_name.split("/")[0]
    )

    repo_name = repository.name

    pull_requests = (
        get_github_pull_requests(
            owner,
            repo_name,
        )
    )

    if not pull_requests:
        return

    for pr in pull_requests:

        PullRequest.objects.update_or_create(

            github_id=pr["id"],

            defaults={

                "repository":
                    repository,

                "title":
                    pr["title"],

                "state":
                    pr["state"],

                "author":
                    (
                        pr["user"]["login"]
                        if pr.get("user")
                        else ""
                    ),

                "created_at":
                    pr["created_at"],

                "updated_at":
                    pr["updated_at"],

                "closed_at":
                    pr["closed_at"],

                "merged_at":
                    pr.get(
                        "merged_at"
                    ),

                "html_url":
                    pr["html_url"],
            }
        )


# =========================================================
# SYNC ISSUES
# =========================================================

def sync_issues(repository):

    owner = (
        repository.full_name.split("/")[0]
    )

    repo_name = repository.name

    issues = get_github_issues(
        owner,
        repo_name,
    )

    if not issues:
        return

    for issue in issues:

        # GitHub's Issues API also returns
        # pull requests.
        if "pull_request" in issue:
            continue

        Issue.objects.update_or_create(

            github_id=issue["id"],

            defaults={

                "repository":
                    repository,

                "title":
                    issue["title"],

                "state":
                    issue["state"],

                "author":
                    (
                        issue["user"]["login"]
                        if issue.get("user")
                        else ""
                    ),

                "created_at":
                    issue["created_at"],

                "updated_at":
                    issue["updated_at"],

                "closed_at":
                    issue["closed_at"],

                "html_url":
                    issue["html_url"],
            }
        )