from django.db.models import Count
from django.db.models.functions import TruncDate

from github_data.models import Commit


def calculate_commit_analytics(developer_profile):

    repositories = developer_profile.repositories.all()

    commits = Commit.objects.filter(
        repository__in=repositories
    )

    total_commits = commits.count()

    # Commits grouped by date
    commits_by_date = (
        commits
        .annotate(date=TruncDate("committed_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    commit_dates = []
    commit_counts = []

    for item in commits_by_date:
        commit_dates.append(
            item["date"].strftime("%Y-%m-%d")
        )
        commit_counts.append(
            item["count"]
        )

    # Average commits per active day
    active_days = len(commit_dates)

    if active_days > 0:
        average_commits_per_day = round(
            total_commits / active_days,
            2
        )
    else:
        average_commits_per_day = 0

    return {
        "total_commits": total_commits,
        "active_days": active_days,
        "average_commits_per_day": average_commits_per_day,
        "commit_dates": commit_dates,
        "commit_counts": commit_counts,
    }