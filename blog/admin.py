# Core Django imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Local application imports
from .models import Blogpost, Comment, MediaCategory, UserProfile


# -----------------------------------------------------------------------------
# Media Category Admin
# Handles the display and management of media categories in admin interface
# -----------------------------------------------------------------------------
@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ("media_name",)
    search_fields = ("media_name",)

# =============================================================================
# Media Category Admin Configuration
# =============================================================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'country')  
    search_fields = ('user__username', 'bio') 


# -----------------------------------------------------------------------------
# Blog Post Admin
# Manages blog posts with rich text editing via Summernote
# -----------------------------------------------------------------------------
@admin.register(Blogpost)
class PostAdmin(SummernoteModelAdmin):
    # Display settings
    list_display = ("blog_title", "slug", "status", "created_on")
    search_fields = ("blog_title", "content")
    prepopulated_fields = {"slug": ("blog_title",)}
    list_filter = ("status", "created_on")
    summernote_fields = "content"


# -----------------------------------------------------------------------------
# Comment Admin
# Handles comment moderation and management
# -----------------------------------------------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Display and filtering options
    list_display = ("user", "body", "blogpost", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ("user", "body", "blogpost")
    actions = ["approved_comments"]

    def approved_comments(self, request, queryset):
        """
        Bulk approve selected comments

        Args:
            request: HTTP request object
            queryset: Selected comment objects to approve
        """
        queryset.update(approved=True)
