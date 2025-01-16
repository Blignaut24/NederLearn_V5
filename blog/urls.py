# Import required Django modules and views
from . import views
from django.urls import path

# Define URL patterns for blog application
urlpatterns = [
    # Root URL pattern "/" maps to PostList view
    # Main landing page: displays list of blog posts
    path("", views.BlogpostPostList.as_view(), name="home"),
    # Single blog post view using URL slugs to display specific posts
    path('<slug:slug>/', views.BlogPostDetail.as_view(), name='blogpost_detail'),
]