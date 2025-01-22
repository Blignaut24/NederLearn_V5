from . import views
from django.urls import path

# Main URL patterns configuration
urlpatterns = [
    # Home
    # ----
    path(
        "", views.BlogpostPostList.as_view(), name="home"
    ),  # Homepage - Displays list of blog posts
    # User Profile Routes
    # ------------------
    path(
        "profile/", views.ProfileView.as_view(), name="profile"
    ),  # Current user profile view
    path(
        "user/<str:username>/",
        views.OtherUserProfileView.as_view(),
        name="other_user_profile",
    ),  # View other users' profiles
    path(
        "profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"
    ),  # Edit profile form
    # Blog Interaction Routes
    # ----------------------
    path(
        "<slug:slug>/", views.BlogPostDetail.as_view(), name="blogpost_detail"
    ),  # Individual blog post view
    path(
        "like/<slug:slug>/", views.LikeUnlike.as_view(), name="like_unlike"
    ),  # Post like/unlike functionality"like_unlike"),
]
