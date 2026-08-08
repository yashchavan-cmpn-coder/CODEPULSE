
from django.urls import path

from .views import (
    home,
    register,
    user_login,
    user_logout,
    profile,
    sync_github_data,
    analyze_code,
)


urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "login/",
        user_login,
        name="login"
    ),

    path(
        "logout/",
        user_logout,
        name="logout"
    ),

    path(
        "profile/",
        profile,
        name="profile"
    ),

    path(
        "sync-github/",
        sync_github_data,
        name="sync_github_data"
    ),

    path(
        "analyze-code/<int:repository_id>/",
        analyze_code,
        name="analyze_code"
    ),
]

