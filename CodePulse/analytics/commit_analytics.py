import pandas as pd

from github_data.models import Commit


def calculate_commit_analytics(developer_profile):

    repositories = (
        developer_profile.repositories.all()
    )

    commits = (
        Commit.objects
        .filter(
            repository__in=repositories
        )
        .values(
            "committed_at"
        )
    )

    data = list(commits)

    # -------------------------------------------------
    # No commits
    # -------------------------------------------------

    if not data:
        return {
            "total_commits": 0,
            "active_days": 0,
            "average_commits_per_day": 0,
            "commit_dates": [],
            "commit_counts": [],
        }

    # -------------------------------------------------
    # Create Pandas DataFrame
    # -------------------------------------------------

    df = pd.DataFrame(data)

    # -------------------------------------------------
    # Convert commit timestamp
    # -------------------------------------------------

    df["committed_at"] = pd.to_datetime(
        df["committed_at"]
    )

    # -------------------------------------------------
    # Extract date
    # -------------------------------------------------

    df["date"] = (
        df["committed_at"]
        .dt.date
    )

    # -------------------------------------------------
    # Group commits by date
    # -------------------------------------------------

    commits_by_date = (
        df.groupby("date")
        .size()
        .reset_index(
            name="count"
        )
    )

    # -------------------------------------------------
    # Total commits
    # -------------------------------------------------

    total_commits = len(df)

    # -------------------------------------------------
    # Active days
    # -------------------------------------------------

    active_days = len(
        commits_by_date
    )

    # -------------------------------------------------
    # Average commits per active day
    # -------------------------------------------------

    if active_days > 0:

        average_commits_per_day = round(
            total_commits / active_days,
            2
        )

    else:

        average_commits_per_day = 0

    # -------------------------------------------------
    # Prepare chart data
    # -------------------------------------------------

    commit_dates = [
        str(date)
        for date in commits_by_date["date"]
    ]

    commit_counts = (
        commits_by_date["count"]
        .tolist()
    )

    # -------------------------------------------------
    # Return analytics
    # -------------------------------------------------

    return {

        "total_commits":
            total_commits,

        "active_days":
            active_days,

        "average_commits_per_day":
            average_commits_per_day,

        "commit_dates":
            commit_dates,

        "commit_counts":
            commit_counts,
    }