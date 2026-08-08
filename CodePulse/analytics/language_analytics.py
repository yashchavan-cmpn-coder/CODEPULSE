from collections import Counter


def calculate_language_analytics(developer_profile):

    repositories = developer_profile.repositories.all()

    languages = []

    for repository in repositories:

        if repository.language:
            languages.append(repository.language)

    language_counts = Counter(languages)

    total_language_repositories = sum(language_counts.values())

    language_data = []

    for language, count in language_counts.most_common():

        percentage = 0

        if total_language_repositories > 0:
            percentage = round(
                (count / total_language_repositories) * 100,
                2
            )

        language_data.append({
            "language": language,
            "count": count,
            "percentage": percentage,
        })

    most_used_language = None

    if language_data:
        most_used_language = language_data[0]["language"]

    return {
        "total_languages": len(language_data),
        "most_used_language": most_used_language,
        "language_data": language_data,
    }