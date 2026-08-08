from .models import (
    CodeQualityAnalysis,
    CodeQualityFile,
)

from .repository_analyzer import (
    analyze_repository,
)


def calculate_quality_score(files):
    high_issues = 0
    medium_issues = 0
    low_issues = 0

    for file_data in files:
        for issue in file_data.get("issues", []):
            if not isinstance(issue, dict):
                continue

            issue_type = str(
                issue.get("type", "")
            ).lower()

            if issue_type in {
                "high complexity",
                "deep nesting",
            }:
                high_issues += 1

            elif issue_type == "long function":
                medium_issues += 1

            else:
                low_issues += 1

    score = 100

    score -= high_issues * 8
    score -= medium_issues * 4
    score -= low_issues * 2

    score = max(
        0,
        min(100, score)
    )

    return {
        "score": score,
        "high": high_issues,
        "medium": medium_issues,
        "low": low_issues,
    }


def save_repository_analysis(
    repository,
    repository_path,
):
    result = analyze_repository(
        repository_path
    )

    files = result.get(
        "files",
        []
    )

    quality = calculate_quality_score(
        files
    )

    analysis, created = (
        CodeQualityAnalysis.objects.update_or_create(
            repository=repository,
            defaults={
                "files_analyzed": result.get(
                    "files_analyzed",
                    0
                ),
                "lines_of_code": result.get(
                    "lines_of_code",
                    0
                ),
                "functions": result.get(
                    "functions",
                    0
                ),
                "classes": result.get(
                    "classes",
                    0
                ),
                "imports": result.get(
                    "imports",
                    0
                ),
                "complexity": result.get(
                    "complexity",
                    0
                ),
                "max_nesting": result.get(
                    "max_nesting",
                    0
                ),
                "languages": result.get(
                    "languages",
                    {}
                ),
                "quality_score": quality[
                    "score"
                ],
                "high_issues": quality[
                    "high"
                ],
                "medium_issues": quality[
                    "medium"
                ],
                "low_issues": quality[
                    "low"
                ],
            },
        )
    )

    analysis.files.all().delete()

    for file_data in files:
        CodeQualityFile.objects.create(
            analysis=analysis,
            file_path=file_data.get(
                "file",
                ""
            ),
            language=file_data.get(
                "language",
                ""
            ),
            lines_of_code=file_data.get(
                "lines_of_code",
                0
            ),
            functions=file_data.get(
                "functions",
                0
            ),
            classes=file_data.get(
                "classes",
                0
            ),
            imports=file_data.get(
                "imports",
                0
            ),
            complexity=file_data.get(
                "complexity",
                0
            ),
            max_nesting=file_data.get(
                "max_nesting",
                0
            ),
            issues=file_data.get(
                "issues",
                []
            ),
        )

    return analysis