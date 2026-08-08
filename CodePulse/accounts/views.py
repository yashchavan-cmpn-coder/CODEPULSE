from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistrationForm, DeveloperProfileForm

from github_data.github_api import (
    sync_repositories,
    sync_commits,
    sync_pull_requests,
    sync_issues,
)

from github_data.analytics import calculate_activity
from github_data.repository_health import calculate_repository_health

from analytics.commit_analytics import calculate_commit_analytics
from analytics.language_analytics import calculate_language_analytics
from analytics.skill_analytics import calculate_skill_analytics
from analytics.productivity_analytics import calculate_productivity_analytics

@login_required
def home(request):
    profile = request.user.developerprofile
    repositories = profile.repositories.all()

    activity = getattr(
        profile,
        "activity",
        None
    )

    return render(
        request,
        "home.html",
        {
            "profile": profile,
            "repositories": repositories,
            "activity": activity,
        }
    )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            user.save()

            login(request, user)

            return redirect("home")
    else:
        form = RegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    developer_profile = request.user.developerprofile

    if request.method == "POST":
        form = DeveloperProfileForm(
            request.POST,
            instance=developer_profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = DeveloperProfileForm(
            instance=developer_profile
        )

    repositories = developer_profile.repositories.all()

    # Repository Health Analysis
    repository_health = []

    for repo in repositories:
        health = calculate_repository_health(repo)

        repository_health.append({
            "repository": repo,
            "health": health,
        })

    # Developer Activity
    activity = calculate_activity(
        developer_profile
    )

    # Commit Analytics
    commit_analytics = calculate_commit_analytics(
        developer_profile
    )

    # Language Analytics
    language_analytics = calculate_language_analytics(
        developer_profile
    )
    # Skill Analytics
    skill_analytics = calculate_skill_analytics(
    developer_profile
    )
    productivity_analytics = calculate_productivity_analytics(
    developer_profile
    )   
    return render(
        request,
        "profile.html",
        {
            "form": form,
            "repositories": repositories,
            "activity": activity,
            "commit_analytics": commit_analytics,
            "language_analytics": language_analytics,
            "skill_analytics": skill_analytics,
            "repository_health": repository_health,
            "productivity_analytics": productivity_analytics,
        }
    )


@login_required
def sync_github_data(request):
    profile = request.user.developerprofile

    sync_repositories(profile)

    repositories = profile.repositories.all()

    for repository in repositories:
        sync_commits(repository)
        sync_pull_requests(repository)
        sync_issues(repository)

    calculate_activity(profile)

    messages.success(
        request,
        "GitHub data synchronized successfully."
    )

    return redirect("home")