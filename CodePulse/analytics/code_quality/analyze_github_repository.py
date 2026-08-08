import os

from .repository_downloader import (
    clone_repository,
    cleanup_repository,
)

from .save_analysis import (
    save_repository_analysis,
)


def analyze_github_repository(
    repository
):
    """
    Clone a GitHub repository, analyze its source
    code, save the results, and clean up the
    temporary repository.
    """

    temporary_directory = None

    try:

        # ========================================
        # Clone repository
        # ========================================

        temporary_directory, repository_path = (
            clone_repository(
                repository.html_url
            )
        )

        # ========================================
        # Analyze repository
        # ========================================

        analysis = save_repository_analysis(
            repository,
            repository_path
        )

        return analysis

    finally:

        # ========================================
        # Remove temporary repository
        # ========================================

        if temporary_directory:

            cleanup_repository(
                temporary_directory
            )