from django.urls import path
from . import views

# Define URL patterns for routing requests
urlpatterns = [
    # HOME
    # -------------------------------------------
    # Main page displaying all blog posts
    path("", views.BlogpostPostList.as_view(), name="home"),
    
    # BLOG POST OPERATIONS
    # -------------------------------------------
    # Create, Read, Update, Delete (CRUD) operations
    path('blogpost/create/', views.BlogpostCreateView.as_view(), name='blogpost_create'),
    path('blogpost/<slug:slug>/', views.BlogPostDetail.as_view(), name='blogpost_detail'),
    path('blogpost/update/<slug:slug>/', views.BlogpostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost/delete/<slug:slug>/', views.BlogpostDeleteView.as_view(), name='blogpost_delete'),

    # INTERACTION
    # -------------------------------------------
    # User interaction with blog posts
    path('blogpost/like/<slug:slug>/', views.LikeUnlike.as_view(), name='like_unlike'),
    path('my-posts/', views.MyBlogPostsView.as_view(), name='my_posts'),

    # USER PROFILES
    # -------------------------------------------
    # Profile viewing and management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user/<str:username>/', views.OtherUserProfileView.as_view(), name='other_user_profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]