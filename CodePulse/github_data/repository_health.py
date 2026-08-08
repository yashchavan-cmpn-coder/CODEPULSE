from django.utils import timezone


def calculate_repository_health(repository):
    """
    Calculate a health score for a single repository.
    Score is based on activity, popularity, maintenance,
    and documentation.
    """

    score = 0

    # --------------------------------
    # 1. Activity Score - 40 points
    # --------------------------------

    if repository.pushed_at:
        now = timezone.now()

        days_since_update = (
            now - repository.pushed_at
        ).days

        if days_since_update <= 7:
            activity_score = 40

        elif days_since_update <= 30:
            activity_score = 30

        elif days_since_update <= 90:
            activity_score = 20

        elif days_since_update <= 180:
            activity_score = 10

        else:
            activity_score = 0

    else:
        activity_score = 0


    # --------------------------------
    # 2. Popularity Score - 25 points
    # --------------------------------

    popularity_score = min(
        repository.stars * 2 +
        repository.forks * 3,
        25
    )


    # --------------------------------
    # 3. Documentation Score - 20 points
    # --------------------------------

    documentation_score = 0

    if repository.description:
        documentation_score += 20


    # --------------------------------
    # 4. Repository Quality - 15 points
    # --------------------------------

    quality_score = 0

    if repository.language:
        quality_score += 5

    if repository.html_url:
        quality_score += 5

    if not repository.is_fork:
        quality_score += 5


    # --------------------------------
    # Final Score
    # --------------------------------

    score = (
        activity_score
        + popularity_score
        + documentation_score
        + quality_score
    )

    return {
        "score": score,
        "activity_score": activity_score,
        "popularity_score": popularity_score,
        "documentation_score": documentation_score,
        "quality_score": quality_score,
    }