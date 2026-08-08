from .models import (
    Commit,
    PullRequest,
    Issue,
    DeveloperActivity,
)


def calculate_activity(developer_profile):
    repositories = developer_profile.repositories.all()

    total_commits = Commit.objects.filter(
        repository__in=repositories
    ).count()

    commit_dates = Commit.objects.filter(
        repository__in=repositories
    ).values_list(
        "committed_at",
        flat=True
    )

    unique_dates = {
        commit_date.date()
        for commit_date in commit_dates
    }

    active_days = len(unique_dates)

    total_pull_requests = PullRequest.objects.filter(
        repository__in=repositories
    ).count()

    total_issues = Issue.objects.filter(
        repository__in=repositories
    ).count()

    # Basic consistency score
    if total_commits > 0:
        consistency_score = min(
            (active_days / total_commits) * 100,
            100
        )
    else:
        consistency_score = 0

    activity, created = DeveloperActivity.objects.get_or_create(
        developer=developer_profile
    )

    activity.total_commits = total_commits
    activity.active_days = active_days
    activity.total_pull_requests = total_pull_requests
    activity.total_issues = total_issues
    activity.consistency_score = round(
        consistency_score,
        2
    )

    activity.save()

    return activity