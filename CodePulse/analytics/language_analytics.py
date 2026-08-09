import pandas as pd
import numpy as np


def calculate_language_analytics(developer_profile):

    repositories = (
        developer_profile.repositories
        .all()
        .values("language")
    )

    # Convert Django QuerySet into a list
    data = list(repositories)

    # No repository data
    if not data:
        return {
            "total_languages": 0,
            "most_used_language": None,
            "language_data": [],
        }

    # Create Pandas DataFrame
    df = pd.DataFrame(data)

    # Remove repositories without a language
    df = df[
        df["language"].notna()
        & (df["language"] != "")
    ]

    # No valid languages
    if df.empty:
        return {
            "total_languages": 0,
            "most_used_language": None,
            "language_data": [],
        }

    # Count repositories for each language
    language_counts = (
        df["language"]
        .value_counts()
        .reset_index()
    )

    language_counts.columns = [
        "language",
        "count",
    ]

    # Calculate total repositories
    total_repositories = (
        language_counts["count"].sum()
    )

    # Calculate percentage using NumPy
    language_counts["percentage"] = np.round(
        (
            language_counts["count"]
            / total_repositories
        ) * 100,
        2,
    )

    # Convert DataFrame to Django-friendly list
    language_data = (
        language_counts
        .to_dict("records")
    )

    # Most used language
    most_used_language = (
        language_counts.iloc[0]["language"]
    )

    return {
        "total_languages": len(
            language_counts
        ),

        "most_used_language":
            most_used_language,

        "language_data":
            language_data,
    }