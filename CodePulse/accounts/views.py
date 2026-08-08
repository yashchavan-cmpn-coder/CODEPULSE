from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import RegistrationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm, DeveloperProfileForm

from django.contrib import messages

from github_data.github_api import (
    sync_repositories,
    sync_commits,
    sync_pull_requests,
    sync_issues,
)

from analytics.commit_analytics import calculate_commit_analytics
from github_data.analytics import calculate_activity


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
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)

            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


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
            {"error": "Invalid username or password."}
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

    activity = calculate_activity(developer_profile)

    commit_analytics = calculate_commit_analytics(
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



