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
from django.conf.urls.static import static
from django.conf import settings
from blog.views import ProfileDeleteView, custom_403_error

from blog.views import index

# Define URL patterns for the entire project
urlpatterns = [
    # Core administrative interface
    path("admin/", admin.site.urls),
    # Maps root URL to blog.urls patterns
    path("", include("blog.urls"), name="blog-urls"),
    # Rich text editor functionality
    path("summernote/", include("django_summernote.urls")),
    # Authentication
    path("accounts/", include("allauth.urls")),
    # Account deletion
    path(
        "account/delete/<int:pk>/", ProfileDeleteView.as_view(), name="account_delete"
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler403 = custom_403_error
