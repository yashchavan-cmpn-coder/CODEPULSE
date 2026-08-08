from .models import (
    CodeQualityAnalysis,
    CodeQualityFile,
)

from .repository_analyzer import (
    analyze_repository,
)


def save_repository_analysis(
    repository,
    repository_path
):
    """
    Analyze a repository and save the
    results to the database.
    """

    # ========================================
    # Run repository analysis
    # ========================================

    result = analyze_repository(
        repository_path
    )

    # ========================================
    # Create / update repository analysis
    # ========================================

    analysis, created = (
        CodeQualityAnalysis.objects.update_or_create(
            repository=repository,
            defaults={
                "files_analyzed": result[
                    "files_analyzed"
                ],

                "lines_of_code": result[
                    "lines_of_code"
                ],

                "functions": result[
                    "functions"
                ],

                "classes": result[
                    "classes"
                ],

                "imports": result[
                    "imports"
                ],

                "complexity": result[
                    "complexity"
                ],

                "max_nesting": result[
                    "max_nesting"
                ],

                "languages": result[
                    "languages"
                ],
            },
        )
    )

    # ========================================
    # Remove old file results
    # ========================================

    analysis.files.all().delete()

    # ========================================
    # Save file-level results
    # ========================================

    for file_data in result.get(
        "files",
        []
    ):

        CodeQualityFile.objects.create(
            analysis=analysis,

            file_path=file_data[
                "file"
            ],

            language=file_data[
                "language"
            ],

            lines_of_code=file_data[
                "lines_of_code"
            ],

            functions=file_data[
                "functions"
            ],

            classes=file_data[
                "classes"
            ],

            imports=file_data[
                "imports"
            ],

            complexity=file_data[
                "complexity"
            ],

            max_nesting=file_data[
                "max_nesting"
            ],

            issues=file_data.get(
                "issues",
                []
            ),
        )

    return analysis