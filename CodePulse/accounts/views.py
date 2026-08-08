
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    RegistrationForm,
    DeveloperProfileForm
)

from github_data.github_api import (
    sync_repositories,
    sync_commits,
    sync_pull_requests,
    sync_issues,
)

from github_data.analytics import (
    calculate_activity
)

from github_data.repository_health import (
    calculate_repository_health
)

from analytics.commit_analytics import (
    calculate_commit_analytics
)

from analytics.language_analytics import (
    calculate_language_analytics
)

from analytics.skill_analytics import (
    calculate_skill_analytics
)

from analytics.productivity_analytics import (
    calculate_productivity_analytics
)

from analytics.code_quality.models import (
    CodeQualityAnalysis
)

from analytics.code_quality.analyze_github_repository import (
    analyze_github_repository
)


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):

    profile = request.user.developerprofile

    # -----------------------------------------------------
    # Repositories
    # -----------------------------------------------------

    repositories = profile.repositories.all()

    # -----------------------------------------------------
    # Developer Activity
    # -----------------------------------------------------

    activity = getattr(
        profile,
        "activity",
        None,
    )

    # -----------------------------------------------------
    # Repository Health
    # -----------------------------------------------------

    repository_health = []

    for repo in repositories:

        health = calculate_repository_health(
            repo
        )

        repository_health.append(
            {
                "repository": repo,
                "health": health,
            }
        )

    # -----------------------------------------------------
    # Commit Analytics
    # -----------------------------------------------------

    commit_analytics = calculate_commit_analytics(
        profile
    )

    # -----------------------------------------------------
    # Language Analytics
    # -----------------------------------------------------

    language_analytics = calculate_language_analytics(
        profile
    )

    # -----------------------------------------------------
    # Skill Analytics
    # -----------------------------------------------------

    skill_analytics = calculate_skill_analytics(
        profile
    )

    # -----------------------------------------------------
    # Productivity Analytics
    # -----------------------------------------------------

    productivity_analytics = (
        calculate_productivity_analytics(
            profile
        )
    )

    # -----------------------------------------------------
    # Code Quality
    # -----------------------------------------------------

    code_quality_analyses = (
        CodeQualityAnalysis.objects
        .filter(
            repository__developer=profile
        )
        .select_related(
            "repository"
        )
        .prefetch_related(
            "files"
        )
    )

    # -----------------------------------------------------
    # Code Quality Summary
    # -----------------------------------------------------

    code_quality_summary = []

    for analysis in code_quality_analyses:

        code_quality_summary.append(
            {
                "repository": analysis.repository,

                "quality_score": (
                    analysis.quality_score
                ),

                "high_issues": (
                    analysis.high_issues
                ),

                "medium_issues": (
                    analysis.medium_issues
                ),

                "low_issues": (
                    analysis.low_issues
                ),

                "files_analyzed": (
                    analysis.files_analyzed
                ),

                "lines_of_code": (
                    analysis.lines_of_code
                ),

                "functions": (
                    analysis.functions
                ),

                "classes": (
                    analysis.classes
                ),

                "imports": (
                    analysis.imports
                ),

                "complexity": (
                    analysis.complexity
                ),

                "max_nesting": (
                    analysis.max_nesting
                ),
            }
        )

    # -----------------------------------------------------
    # Dashboard
    # -----------------------------------------------------

    return render(
        request,
        "home.html",
        {
            "profile": profile,

            "repositories": repositories,

            "activity": activity,

            "repository_health": repository_health,

            "commit_analytics": commit_analytics,

            "language_analytics": language_analytics,

            "skill_analytics": skill_analytics,

            "productivity_analytics": (
                productivity_analytics
            ),

            "code_quality_analyses": (
                code_quality_analyses
            ),

            "code_quality_summary": (
                code_quality_summary
            ),
        },
    )



# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = RegistrationForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error":
                    "Invalid username or password."
            }
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect("login")


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    developer_profile = (
        request.user.developerprofile
    )

    # -----------------------------------------------------
    # Profile form
    # -----------------------------------------------------

    if request.method == "POST":

        form = DeveloperProfileForm(
            request.POST,
            instance=developer_profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                "profile"
            )

    else:

        form = DeveloperProfileForm(
            instance=developer_profile
        )

    # -----------------------------------------------------
    # Repositories
    # -----------------------------------------------------

    repositories = (
        developer_profile.repositories.all()
    )

    # -----------------------------------------------------
    # Repository Health
    # -----------------------------------------------------

    repository_health = []

    for repo in repositories:

        health = (
            calculate_repository_health(
                repo
            )
        )

        repository_health.append({

            "repository": repo,

            "health": health,

        })

    # -----------------------------------------------------
    # Developer Activity
    # -----------------------------------------------------

    activity = calculate_activity(
        developer_profile
    )

    # -----------------------------------------------------
    # Commit Analytics
    # -----------------------------------------------------

    commit_analytics = (
        calculate_commit_analytics(
            developer_profile
        )
    )

    # -----------------------------------------------------
    # Language Analytics
    # -----------------------------------------------------

    language_analytics = (
        calculate_language_analytics(
            developer_profile
        )
    )

    # -----------------------------------------------------
    # Skill Analytics
    # -----------------------------------------------------

    skill_analytics = (
        calculate_skill_analytics(
            developer_profile
        )
    )

    # -----------------------------------------------------
    # Productivity Analytics
    # -----------------------------------------------------

    productivity_analytics = (
        calculate_productivity_analytics(
            developer_profile
        )
    )

    # -----------------------------------------------------
    # Code Quality
    #
    # IMPORTANT:
    # We ONLY read saved results here.
    #
    # No repository cloning.
    # No source-code scanning.
    # No AST analysis.
    # -----------------------------------------------------

    code_quality_analyses = (
        CodeQualityAnalysis.objects
        .filter(
            repository__developer=
            developer_profile
        )
        .prefetch_related(
            "files"
        )
    )

    # -----------------------------------------------------
    # Render Profile
    # -----------------------------------------------------

    return render(
        request,
        "profile.html",
        {
            "form": form,

            "repositories":
                repositories,

            "activity":
                activity,

            "commit_analytics":
                commit_analytics,

            "language_analytics":
                language_analytics,

            "skill_analytics":
                skill_analytics,

            "repository_health":
                repository_health,

            "productivity_analytics":
                productivity_analytics,

            "code_quality_analyses":
                code_quality_analyses,
        }
    )


# =========================================================
# SYNC GITHUB DATA
# =========================================================

@login_required
def sync_github_data(request):

    profile = (
        request.user.developerprofile
    )

    # -----------------------------------------------------
    # Sync repositories
    # -----------------------------------------------------

    sync_repositories(
        profile
    )

    repositories = (
        profile.repositories.all()
    )

    # -----------------------------------------------------
    # Sync repository data
    # -----------------------------------------------------

    for repository in repositories:

        sync_commits(
            repository
        )

        sync_pull_requests(
            repository
        )

        sync_issues(
            repository
        )

    # -----------------------------------------------------
    # Recalculate activity
    # -----------------------------------------------------

    calculate_activity(
        profile
    )

    messages.success(
        request,
        "GitHub data synchronized successfully."
    )

    return redirect(
        "home"
    )


# =========================================================
# ANALYZE CODE
# =========================================================

@login_required
def analyze_code(
    request,
    repository_id
):

    profile = (
        request.user.developerprofile
    )

    # -----------------------------------------------------
    # Security:
    # Only allow the current developer to analyze
    # their own repository.
    # -----------------------------------------------------

    repository = (
        profile.repositories
        .filter(
            id=repository_id
        )
        .first()
    )

    if repository is None:

        messages.error(
            request,
            "Repository not found."
        )

        return redirect(
            "profile"
        )

    # -----------------------------------------------------
    # Run Code Quality Analysis
    # -----------------------------------------------------

    try:

        analyze_github_repository(
            repository
        )

        messages.success(
            request,
            f"Code analysis completed for "
            f"{repository.name}."
        )

    except Exception as error:

        messages.error(
            request,
            f"Code analysis failed: {error}"
        )

    return redirect(
        "profile"
    )
