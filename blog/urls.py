from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    # =================================================================
    # Home Page
    # =================================================================
    # Main landing page that displays all blog posts in a list format
    path("", views.BlogpostPostList.as_view(), name="home"),
    
    # =================================================================
    # Blog Post Management
    # =================================================================
    # CRUD operations for blog posts:
    # - Create: Add new blog posts
    # - Read: View individual blog posts
    # - Update: Edit existing blog posts
    # - Delete: Remove blog posts
    path('blogpost/create/', views.BlogpostCreateView.as_view(), name='blogpost_create'),
    path('blogpost/<slug:slug>/', views.BlogPostDetail.as_view(), name='blogpost_detail'),
    path('blogpost/update/<slug:slug>/', views.BlogpostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost/delete/<slug:slug>/', views.BlogpostDeleteView.as_view(), name='blogpost_delete'),

    # =================================================================
    # User Interactions
    # =================================================================
    # Endpoints for user engagement with blog content:
    # - Like/Unlike functionality
    # - Personal post management
    path('blogpost/like/<slug:slug>/', views.LikeUnlike.as_view(), name='like_unlike'),
    path('my-posts/', views.MyBlogPostsView.as_view(), name='my_posts'),

    # =================================================================
    # User Profile Management
    # =================================================================
    # Routes for handling user profile operations:
    # - View own profile
    # - View other users' profiles
    # - Edit profile settings
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user/<str:username>/', views.OtherUserProfileView.as_view(), name='other_user_profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('about-us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
     # Display the 'Saved For Later' page
    path('saved-for-later/', views.bookmarked, name='bookmarked'),
    
    # Bookmark or un-bookmark a post
    path('bookmark-unbookmark/<slug:slug>/', views.BookmarkUnbookmark.as_view(), name='bookmark_unbookmark'),
]