
import os

from .analyzer import analyze_file


# --------------------------------
# Directories excluded from analysis
# --------------------------------

EXCLUDED_DIRECTORIES = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    "migrations",
    "node_modules",
    "dist",
    "build",
}


# --------------------------------
# Files excluded from analysis
# --------------------------------

EXCLUDED_FILES = {
    "test_code_quality.py",
}


# --------------------------------
# Internal CodePulse directories
# --------------------------------

EXCLUDED_PATHS = {
    os.path.normpath(
        os.path.join(
            "analytics",
            "code_quality"
        )
    ),
}


# --------------------------------
# Supported languages
# --------------------------------

LANGUAGE_EXTENSIONS = {
    ".py": "Python",

    ".js": "JavaScript",
    ".jsx": "JavaScript",

    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    ".java": "Java",

    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".h": "C++",
    ".hpp": "C++",
}


def should_exclude_directory(
    directory_path,
    repository_path
):
    """
    Determine whether a directory should
    be excluded from analysis.
    """

    relative_path = os.path.relpath(
        directory_path,
        repository_path
    )

    relative_path = os.path.normpath(
        relative_path
    )

    parts = relative_path.split(
        os.sep
    )

    # Exclude directories such as
    # venv, migrations, __pycache__, etc.
    if any(
        part in EXCLUDED_DIRECTORIES
        for part in parts
    ):
        return True

    # Exclude CodePulse's own
    # code-quality analyzer
    for excluded_path in EXCLUDED_PATHS:

        if (
            relative_path == excluded_path
            or relative_path.startswith(
                excluded_path + os.sep
            )
        ):
            return True

    return False


def analyze_repository(repository_path):
    """
    Analyze supported source files
    inside a repository.
    """

    result = {

        # --------------------------------
        # Repository-level metrics
        # --------------------------------

        "files_analyzed": 0,
        "lines_of_code": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "complexity": 0,
        "max_nesting": 0,

        # --------------------------------
        # Repository issues
        # --------------------------------

        "issues": [],

        # --------------------------------
        # Language statistics
        # --------------------------------

        "languages": {},

        # --------------------------------
        # Individual file results
        # --------------------------------

        "files": [],
    }

    # --------------------------------
    # Check repository path
    # --------------------------------

    if not os.path.exists(repository_path):

        result["error"] = (
            "Repository path does not exist."
        )

        return result

    if not os.path.isdir(repository_path):

        result["error"] = (
            "Repository path is not a directory."
        )

        return result

    # --------------------------------
    # Walk through repository
    # --------------------------------

    for root, directories, files in os.walk(
        repository_path
    ):

        # --------------------------------
        # Remove excluded directories
        # --------------------------------

        directories[:] = [
            directory
            for directory in directories
            if not should_exclude_directory(
                os.path.join(
                    root,
                    directory
                ),
                repository_path
            )
        ]

        # --------------------------------
        # Process files
        # --------------------------------

        for filename in files:

            # Skip explicitly excluded files
            if filename in EXCLUDED_FILES:
                continue

            extension = os.path.splitext(
                filename
            )[1].lower()

            language = LANGUAGE_EXTENSIONS.get(
                extension
            )

            # Skip unsupported files
            if not language:
                continue

            file_path = os.path.join(
                root,
                filename
            )

            # --------------------------------
            # Analyze file
            # --------------------------------

            analysis = analyze_file(
                file_path,
                language
            )

            # --------------------------------
            # Relative file path
            # --------------------------------

            relative_path = os.path.relpath(
                file_path,
                repository_path
            )

            relative_path = os.path.normpath(
                relative_path
            )

            # --------------------------------
            # File-level result
            # --------------------------------

            file_result = {
                "file": relative_path,
                "language": language,

                "supported": analysis.get(
                    "supported",
                    False
                ),

                "lines_of_code": analysis.get(
                    "lines_of_code",
                    0
                ),

                "functions": analysis.get(
                    "functions",
                    0
                ),

                "classes": analysis.get(
                    "classes",
                    0
                ),

                "imports": analysis.get(
                    "imports",
                    0
                ),

                "complexity": analysis.get(
                    "complexity",
                    0
                ),

                "max_nesting": analysis.get(
                    "max_nesting",
                    0
                ),

                "issues": analysis.get(
                    "issues",
                    []
                ),
            }

            result["files"].append(
                file_result
            )

            # --------------------------------
            # Only aggregate supported files
            # --------------------------------

            if not analysis.get(
                "supported",
                False
            ):
                continue

            result["files_analyzed"] += 1

            # --------------------------------
            # Aggregate metrics
            # --------------------------------

            result["lines_of_code"] += (
                analysis.get(
                    "lines_of_code",
                    0
                )
            )

            result["functions"] += (
                analysis.get(
                    "functions",
                    0
                )
            )

            result["classes"] += (
                analysis.get(
                    "classes",
                    0
                )
            )

            result["imports"] += (
                analysis.get(
                    "imports",
                    0
                )
            )

            result["complexity"] += (
                analysis.get(
                    "complexity",
                    0
                )
            )

            result["max_nesting"] = max(
                result["max_nesting"],
                analysis.get(
                    "max_nesting",
                    0
                )
            )

            # --------------------------------
            # Collect issues
            # --------------------------------

            for issue in analysis.get(
                "issues",
                []
            ):

                if isinstance(
                    issue,
                    dict
                ):

                    issue = issue.copy()

                    issue["file"] = (
                        relative_path
                    )

                result["issues"].append(
                    issue
                )

            # --------------------------------
            # Language statistics
            # --------------------------------

            if language not in result[
                "languages"
            ]:

                result["languages"][language] = {
                    "files": 0,
                    "lines": 0,
                }

            result["languages"][language][
                "files"
            ] += 1

            result["languages"][language][
                "lines"
            ] += analysis.get(
                "lines_of_code",
                0
            )

    return result

