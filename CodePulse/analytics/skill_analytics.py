def calculate_skill_analytics(developer_profile):
    repositories = developer_profile.repositories.all()

    language_stats = {}

    for repo in repositories:

        if not repo.language:
            continue

        language = repo.language

        if language not in language_stats:
            language_stats[language] = {
                "repositories": 0,
                "stars": 0,
                "forks": 0,
                "commits": 0,
            }

        language_stats[language]["repositories"] += 1
        language_stats[language]["stars"] += repo.stars
        language_stats[language]["forks"] += repo.forks

        language_stats[language]["commits"] += (
            repo.commits.count()
        )

    skill_data = []

    for language, stats in language_stats.items():

        repository_score = min(
            stats["repositories"] * 20,
            40
        )

        commit_score = min(
            stats["commits"] * 2,
            30
        )

        popularity_score = min(
            stats["stars"] + stats["forks"],
            30
        )

        skill_score = (
            repository_score
            + commit_score
            + popularity_score
        )

        skill_data.append({
            "language": language,
            "repositories": stats["repositories"],
            "commits": stats["commits"],
            "stars": stats["stars"],
            "forks": stats["forks"],
            "score": skill_score,
        })

    skill_data.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "skills": skill_data,
        "total_skills": len(skill_data),
    }