"""
NederLearn URL Configuration
=====================================

This module handles URL routing for the NederLearn application.

For detailed Django URL configuration docs, see:
https://docs.djangoproject.com/en/3.2/topics/http/urls/

URL Pattern Types:
-----------------
1. Function-based Views:
   from my_app import views
   path('', views.home, name='home')

2. Class-based Views:  
   from other_app.views import Home
   path('', Home.as_view(), name='home')

3. Including Other URLconfs:
   from django.urls import include
   path('blog/', include('blog.urls'))
"""

# Django Core Imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# Local App Imports 
from blog.views import ProfileDeleteView, custom_403_error

# Main URL Patterns
urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Blog URLs (Root URL Pattern)
    path("", include("blog.urls"), name="blog-urls"),
    
    # Rich Text Editor
    path('summernote/', include('django_summernote.urls')),
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),
    
    # Profile Management 
    path(
        'account/delete/<int:pk>/',
        ProfileDeleteView.as_view(),
        name='account_delete'
    ),
]

# Development Media File Serving
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Custom Error Handlers
handler403 = custom_403_error  # Forbidden Error Handler_error