from django.contrib import admin

# Register your models here.

from .models import Repository



from .models import Repository, Commit, PullRequest,Issue


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "developer",
        "language",
        "stars",
        "forks",
        "is_fork",
    )

    search_fields = (
        "name",
        "full_name",
        "developer__user__username",
    )

    list_filter = (
        "language",
        "is_fork",
    )


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "author_name",
        "committed_at",
        "message",
    )

    search_fields = (
        "message",
        "author_name",
        "repository__name",
    )

    list_filter = (
        "repository",
        "committed_at",
    )


@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "title",
        "author",
        "state",
        "created_at",
        "merged_at",
    )

    search_fields = (
        "title",
        "author",
        "repository__name",
    )

    list_filter = (
        "state",
        "repository",
    )



@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "title",
        "author",
        "state",
        "created_at",
        "closed_at",
    )

    search_fields = (
        "title",
        "author",
        "repository__name",
    )

    list_filter = (
        "state",
        "repository",
    )

