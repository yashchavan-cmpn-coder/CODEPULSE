def calculate_productivity_analytics(developer_profile):
    repositories = developer_profile.repositories.all()

    # --------------------------------
    # Collect GitHub activity
    # --------------------------------

    total_commits = 0
    total_pull_requests = 0
    merged_pull_requests = 0
    total_issues = 0
    closed_issues = 0

    for repo in repositories:

        total_commits += repo.commits.count()

        pull_requests = repo.pull_requests.all()

        total_pull_requests += pull_requests.count()

        merged_pull_requests += pull_requests.filter(
            merged_at__isnull=False
        ).count()

        issues = repo.issues.all()

        total_issues += issues.count()

        closed_issues += issues.filter(
            state="closed"
        ).count()

    # --------------------------------
    # Commit Score - 30 points
    # --------------------------------

    commit_score = min(
        total_commits * 3,
        30
    )

    # --------------------------------
    # Pull Request Score - 25 points
    # --------------------------------

    pull_request_score = min(
        total_pull_requests * 5,
        25
    )

    # --------------------------------
    # PR Merge Rate - 20 points
    # --------------------------------

    if total_pull_requests > 0:
        merge_rate = round(
            (merged_pull_requests / total_pull_requests) * 100,
            2
        )
    else:
        merge_rate = 0

    merge_score = round(
        (merge_rate / 100) * 20,
        2
    )

    # --------------------------------
    # Issue Resolution - 15 points
    # --------------------------------

    if total_issues > 0:
        issue_resolution_rate = round(
            (closed_issues / total_issues) * 100,
            2
        )
    else:
        issue_resolution_rate = 0

    issue_score = round(
        (issue_resolution_rate / 100) * 15,
        2
    )

    # --------------------------------
    # Consistency - 10 points
    # --------------------------------

    activity = getattr(
        developer_profile,
        "activity",
        None
    )

    if activity:
        consistency_score = min(
            activity.consistency_score,
            10
        )
    else:
        consistency_score = 0

    # --------------------------------
    # Final Productivity Score
    # --------------------------------

    productivity_score = round(
        commit_score
        + pull_request_score
        + merge_score
        + issue_score
        + consistency_score,
        2
    )

    return {
        "productivity_score": productivity_score,

        "total_commits": total_commits,

        "total_pull_requests": total_pull_requests,

        "merged_pull_requests": merged_pull_requests,

        "merge_rate": merge_rate,

        "total_issues": total_issues,

        "closed_issues": closed_issues,

        "issue_resolution_rate": issue_resolution_rate,

        "commit_score": commit_score,

        "pull_request_score": pull_request_score,

        "merge_score": merge_score,

        "issue_score": issue_score,

        "consistency_score": consistency_score,
    }