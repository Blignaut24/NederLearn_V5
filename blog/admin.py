from django.contrib import admin
from .models import Blogpost
from django_summernote.admin import SummernoteModelAdmin

"""
Configures blog post admin with Summernote rich text editor.
"""


@admin.register(Blogpost)
class PostAdmin(SummernoteModelAdmin):
    """Admin config for blog posts with Summernote editor."""

    summernote_fields = ("content",)  # Enable rich text for content field
