from django.db import models

# Create your models here.
from django.db import models
from accounts.models import DeveloperProfile


class Repository(models.Model):
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name="repositories"
    )

    github_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    html_url = models.URLField()
    language = models.CharField(max_length=100, blank=True)

    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)

    is_fork = models.BooleanField(default=False)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name
    

class Commit(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="commits"
    )

    github_sha = models.CharField(
        max_length=40,
        unique=True
    )

    message = models.TextField()

    author_name = models.CharField(
        max_length=255,
        blank=True
    )

    author_email = models.EmailField(
        blank=True
    )

    committed_at = models.DateTimeField()

    html_url = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.message[:50]
    

class PullRequest(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="pull_requests"
    )

    github_id = models.BigIntegerField(unique=True)

    title = models.CharField(max_length=500)

    state = models.CharField(max_length=20)

    author = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    merged_at = models.DateTimeField(
        null=True,
        blank=True
    )

    html_url = models.URLField()

    def __str__(self):
        return self.title
    


class Issue(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    github_id = models.BigIntegerField(unique=True)

    title = models.CharField(max_length=500)

    state = models.CharField(max_length=20)

    author = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    html_url = models.URLField()

    def __str__(self):
        return self.title
    

class DeveloperActivity(models.Model):
    developer = models.OneToOneField(
        "accounts.DeveloperProfile",
        on_delete=models.CASCADE,
        related_name="activity"
    )

    total_commits = models.PositiveIntegerField(default=0)

    active_days = models.PositiveIntegerField(default=0)

    total_pull_requests = models.PositiveIntegerField(default=0)

    total_issues = models.PositiveIntegerField(default=0)

    consistency_score = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.developer.github_username} Activity"