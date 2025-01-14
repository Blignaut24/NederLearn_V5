# Import required Django modules and views
from . import views
from django.urls import path

# Define URL patterns for blog application
urlpatterns = [
    # Root URL pattern "/" maps to PostList view
    # Main landing page: displays list of blog posts
    path("", views.PostList.as_view(), name="home"),
]