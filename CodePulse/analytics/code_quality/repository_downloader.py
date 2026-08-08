import os
import shutil
import tempfile

from git import Repo


def clone_repository(repository_url):
    """
    Clone a GitHub repository into a temporary directory.

    Returns:
        tuple:
            temporary_directory,
            repository_path
    """

    temporary_directory = tempfile.mkdtemp(
        prefix="codepulse_"
    )

    repository_path = os.path.join(
        temporary_directory,
        "repository"
    )

    try:

        Repo.clone_from(
            repository_url,
            repository_path,
            depth=1
        )

        return (
            temporary_directory,
            repository_path
        )

    except Exception:

        shutil.rmtree(
            temporary_directory,
            ignore_errors=True
        )

        raise


def cleanup_repository(
    temporary_directory
):
    """
    Delete the temporary cloned repository.
    """

    shutil.rmtree(
        temporary_directory,
        ignore_errors=True
    )