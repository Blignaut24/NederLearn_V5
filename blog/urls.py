# ==================================
# Django URL Configuration
# ==================================

from django.urls import path
from django.views.generic.base import TemplateView
from . import views

# URL patterns for routing requests to appropriate views
urlpatterns = [
    # Home/Landing Page
    # ----------------
    path("", views.BlogPostList.as_view(), name="home"),
    # Blog Post Management
    # -------------------
    # Create new post
    path(
        "blogpost/create/",
        views.BlogpostCreateView.as_view(),
        name="blogpost_create",
    ),
    # View single post
    path(
        "blogpost/<slug:slug>/",
        views.BlogPostDetail.as_view(),
        name="blogpost_detail",
    ),
    # Update existing post
    path(
        "blogpost/update/<slug:slug>/",
        views.BlogpostUpdateView.as_view(),
        name="blogpost_update",
    ),
    # Delete post
    path(
        "blogpost/delete/<slug:slug>/",
        views.BlogpostDeleteView.as_view(),
        name="blogpost_delete",
    ),
    # User Content Management
    # ----------------------
    # View user's posts
    path("my-posts/", views.MyBlogPostsView.as_view(), name="my_posts"),
    # Post Interaction
    # ---------------
    # Like/Unlike posts
    path(
        "blogpost/like/<slug:slug>/",
        views.LikeUnlike.as_view(),
        name="like_unlike",
    ),
    # User Profile Management
    # ----------------------
    # View own profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    # View other user profiles
    path(
        "user/<str:username>/",
        views.OtherUserProfileView.as_view(),
        name="other_user_profile",
    ),
    # Edit profile
    path(
        "profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"
    ),
    # Static Pages
    # -----------
    # About page
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about_us",
    ),
    # Content Management
    # -----------------
    # View saved posts
    path("saved-for-later/", views.bookmarked, name="bookmarked"),
    # Bookmark management
    path(
        "bookmark-unbookmark/<slug:slug>/",
        views.BookmarkUnbookmark.as_view(),
        name="bookmark_unbookmark",
    ),
]
