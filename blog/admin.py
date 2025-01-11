# Django imports
from django.contrib import admin
from .models import Blogpost, Comment
from django_summernote.admin import SummernoteModelAdmin

# ------------------------------------------------------------------------
# Blog Post Admin Configuration
# ------------------------------------------------------------------------


@admin.register(Blogpost)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for managing blog posts.
    Includes rich text editing via Summernote.
    """

    # Display settings for admin list view
    list_display = ("blog_title", "slug", "status", "created_on")

    # Search functionality configuration
    search_fields = ("blog_title", "content")

    # Auto-populate slug field from blog title
    prepopulated_fields = {"slug": ("blog_title",)}

    # Filter options in admin sidebar
    list_filter = ("status", "created_on")

    # Enable Summernote rich text editor for content field
    summernote_fields = "content"


# ------------------------------------------------------------------------
# Comment Admin Configuration
# ------------------------------------------------------------------------


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing user comments.
    Includes comment moderation capabilities.
    """

    # Display settings for admin list view
    list_display = ("user", "body", "post", "created_on", "approved")

    # Filter options in admin sidebar
    list_filter = ("approved", "created_on")

    # Search functionality configuration
    search_fields = ("user", "body", "post")

    # Available admin actions
    actions = ["approved_comments"]

    def approved_comments(self, request, queryset):
        """
        Bulk action to approve selected comments.
        Updates approved status to True for all selected comments.
        """
        queryset.update(approved=True)
