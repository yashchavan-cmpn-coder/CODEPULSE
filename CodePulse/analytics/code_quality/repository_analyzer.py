import os

from .analyzer import analyze_file


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


def analyze_repository(repository_path):
    """
    Analyze all supported source files
    inside a repository.
    """

    result = {
        # Repository-level metrics
        "files_analyzed": 0,
        "lines_of_code": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "complexity": 0,
        "max_nesting": 0,

        # Issues across repository
        "issues": [],

        # Language statistics
        "languages": {},

        # Individual file results
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

    # --------------------------------
    # Walk through repository
    # --------------------------------

    for root, directories, files in os.walk(
        repository_path
    ):

        # Ignore unnecessary directories
        directories[:] = [
            directory
            for directory in directories
            if directory not in {
                ".git",
                "node_modules",
                "venv",
                ".venv",
                "__pycache__",
                "dist",
                "build",
            }
        ]

        for filename in files:

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

            # Relative path inside repository
            relative_path = os.path.relpath(
                file_path,
                repository_path
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
            # Count analyzed files
            # --------------------------------

            if analysis.get(
                "supported",
                False
            ):

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

                if isinstance(issue, dict):

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