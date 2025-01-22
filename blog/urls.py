# Django URL Configuration
# This module defines URL patterns for the blog application

from . import views
from django.urls import path

# URL patterns for routing HTTP requests
urlpatterns = [
    # Main views
    path(
        "", views.BlogpostPostList.as_view(), name="home"
    ),  # Homepage - displays list of blog posts
    path(
        "profile/", views.ProfileView.as_view(), name="profile"
    ),  # User's own profile page
    # User-related views
    path(
        "user/<str:username>/",
        views.OtherUserProfileView.as_view(),
        name="other_user_profile",
    ),  # View other user profiles
    # Blog post views
    path(
        "<slug:slug>/", views.BlogPostDetail.as_view(), name="blogpost_detail"
    ),  # Individual blog post page
    path("like/<slug:slug>/", views.LikeUnlike.as_view(), name="like_unlike"),
]
