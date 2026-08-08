from django.db import models


class CodeQualityAnalysis(models.Model):
    """
    Stores the latest code quality analysis
    for a developer repository.
    """

    repository = models.OneToOneField(
        "github_data.Repository",
        on_delete=models.CASCADE,
        related_name="code_quality",
    )

    files_analyzed = models.PositiveIntegerField(default=0)
    lines_of_code = models.PositiveIntegerField(default=0)
    functions = models.PositiveIntegerField(default=0)
    classes = models.PositiveIntegerField(default=0)
    imports = models.PositiveIntegerField(default=0)

    complexity = models.PositiveIntegerField(default=0)
    max_nesting = models.PositiveIntegerField(default=0)

    languages = models.JSONField(default=dict)

    analyzed_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Code Quality - "
            f"{self.repository.name}"
        )


class CodeQualityFile(models.Model):
    """
    Stores code quality analysis for
    individual source files.
    """

    analysis = models.ForeignKey(
        CodeQualityAnalysis,
        on_delete=models.CASCADE,
        related_name="files",
    )

    file_path = models.CharField(
        max_length=500
    )

    language = models.CharField(
        max_length=50
    )

    lines_of_code = models.PositiveIntegerField(
        default=0
    )

    functions = models.PositiveIntegerField(
        default=0
    )

    classes = models.PositiveIntegerField(
        default=0
    )

    imports = models.PositiveIntegerField(
        default=0
    )

    complexity = models.PositiveIntegerField(
        default=0
    )

    max_nesting = models.PositiveIntegerField(
        default=0
    )

    issues = models.JSONField(
        default=list
    )

    def __str__(self):
        return self.file_path