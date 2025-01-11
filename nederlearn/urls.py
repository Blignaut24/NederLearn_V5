"""
URLs Configuration
-----------------

Main URL routing configuration for the CodeStar project. Maps URLs to their 
corresponding views and includes other URL configurations.

Routes:
- /admin/      -> Django admin interface
- /           -> Main index view
- /summernote/ -> Rich text editor URLs

For Django URL patterns documentation:
https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

from blog.views import index

# Define URL patterns for the entire project
urlpatterns = [
    # Core administrative interface
    path("admin/", admin.site.urls),
    # Main landing page
    path("", index),
    # Rich text editor functionality
    path("summernote/", include("django_summernote.urls")),
]
