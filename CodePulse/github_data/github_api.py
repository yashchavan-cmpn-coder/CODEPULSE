import requests

from .models import Repository, Commit , PullRequest ,Issue


GITHUB_API_URL = "https://api.github.com"


def get_github_user(username):
    url = f"{GITHUB_API_URL}/users/{username}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None


def get_github_repositories(username):
    url = f"{GITHUB_API_URL}/users/{username}/repos"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return []


def sync_repositories(developer_profile):
    repositories = get_github_repositories(
        developer_profile.github_username
    )

    for repo in repositories:
        Repository.objects.update_or_create(
            github_id=repo["id"],
            defaults={
                "developer": developer_profile,
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"] or "",
                "html_url": repo["html_url"],
                "language": repo["language"] or "",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "is_fork": repo["fork"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "pushed_at": repo["pushed_at"],
            }
        )


def get_github_commits(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return []


def sync_commits(repository):
    owner = repository.full_name.split("/")[0]
    repo_name = repository.name

    commits = get_github_commits(owner, repo_name)

    for commit_data in commits:
        commit_info = commit_data["commit"]
        author = commit_info.get("author") or {}

        Commit.objects.update_or_create(
            github_sha=commit_data["sha"],
            defaults={
                "repository": repository,
                "message": commit_info.get("message", ""),
                "author_name": author.get("name", ""),
                "author_email": author.get("email", ""),
                "committed_at": author.get("date"),
                "html_url": commit_data.get("html_url", ""),
            }
        )


def get_github_pull_requests(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"

    params = {
        "state": "all"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return []


def get_github_issues(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"

    params = {
        "state": "all"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return []



def sync_pull_requests(repository):
    owner = repository.full_name.split("/")[0]
    repo_name = repository.name

    pull_requests = get_github_pull_requests(
        owner,
        repo_name
    )

    for pr in pull_requests:
        PullRequest.objects.update_or_create(
            github_id=pr["id"],
            defaults={
                "repository": repository,
                "title": pr["title"],
                "state": pr["state"],
                "author": (
                    pr["user"]["login"]
                    if pr.get("user")
                    else ""
                ),
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "closed_at": pr["closed_at"],
                "merged_at": pr.get("merged_at"),
                "html_url": pr["html_url"],
            }
        )


def sync_issues(repository):
    owner = repository.full_name.split("/")[0]
    repo_name = repository.name

    issues = get_github_issues(
        owner,
        repo_name
    )

    for issue in issues:
        Issue.objects.update_or_create(
            github_id=issue["id"],
            defaults={
                "repository": repository,
                "title": issue["title"],
                "state": issue["state"],
                "author": (
                    issue["user"]["login"]
                    if issue.get("user")
                    else ""
                ),
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "closed_at": issue["closed_at"],
                "html_url": issue["html_url"],
            }
        )