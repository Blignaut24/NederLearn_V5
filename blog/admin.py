# Core Django imports
from django.contrib import admin
from .models import Blogpost, Comment, MediaCategory
from django_summernote.admin import SummernoteModelAdmin


# -----------------------------------------------------------------------------
# Media Category Admin
# -----------------------------------------------------------------------------
@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    """Handles media category management in admin panel"""

    list_display = ("media_name",)
    search_fields = ("media_name",)


# -----------------------------------------------------------------------------
# Blog Post Admin
# -----------------------------------------------------------------------------
@admin.register(Blogpost)
class PostAdmin(SummernoteModelAdmin):
    """
    Blog post management configuration
    Features:
    - Rich text editing with Summernote
    - Automatic slug generation
    - Filtering and search capabilities
    """

    # Admin list view configuration
    list_display = ("blog_title", "slug", "status", "created_on")
    search_fields = ("blog_title", "content")
    prepopulated_fields = {"slug": ("blog_title",)}
    list_filter = ("status", "created_on")

    # Rich text editor field
    summernote_fields = "content"


# -----------------------------------------------------------------------------
# Comment Admin
# -----------------------------------------------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment management configuration
    Features:
    - Comment moderation system
    - Bulk approval functionality
    - Filtering and search capabilities
    """

    # Admin list view configuration
    list_display = ("user", "body", "post", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ("user", "body", "post")
    actions = ["approved_comments"]

    def approved_comments(self, request, queryset):
        """Bulk approve selected comments"""
        queryset.update(approved=True)
