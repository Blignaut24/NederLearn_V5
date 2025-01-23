from django import forms
from .models import Comment, UserProfile, Blogpost
import datetime


class BlogpostForm(forms.ModelForm):
    """
    Blog Post Creation/Edit Form
    ---------------------------
    Handles the creation and editing of blog posts with customized fields and widgets.

    Fields:
        - blog_title: Title of the blog post
        - content: Main blog content (max 2000 chars)
        - excerpt: Short summary (max 100 chars)
        - status: Publication status
        - featured_image: Header image
        - media_category: Type of media being reviewed
        - release_year: Year of media release (1800-present)
        - media_link: URL to referenced media
    """

    class Meta:
        model = Blogpost
        fields = [
            "blog_title",
            "content",
            "excerpt",
            "status",
            "featured_image",
            "media_category",
            "release_year",
            "media_link",
        ]

        widgets = {
            "blog_title": forms.TextInput(
                attrs={"placeholder": "Enter the title of the blog post..."}
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your blog content here (max length 2000 characters)...",
                    "maxlength": "2000",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Write a short excerpt...(max length 100 characters)",
                    "maxlength": "100",
                }
            ),
            "release_year": forms.NumberInput(
                attrs={
                    "min": 1800,
                    "max": datetime.datetime.now().year,
                    "placeholder": "YYYY",
                }
            ),
            "media_link": forms.URLInput(
                attrs={"placeholder": "http://www.example.com"}
            ),
        }
        # Remove labels for cleaner UI
        labels = {
            "blog_title": "",
            "content": "",
            "excerpt": "",
            "release_year": "",
            "media_link": "",
        }


class CommentForm(forms.ModelForm):
    """
    Comment Form
    -----------
    Handles user comments on blog posts.

    Features:
        - Single text field for comment body
        - Character limit: 1500
        - Responsive textarea (2 rows x 50 columns)
        - Custom placeholder text
    """

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 2,
                    "cols": 50,
                    "placeholder": "Drop your thoughts here like they're hot! 🔥",
                    "max_length": "1500",
                }
            ),
        }
        labels = {
            "body": "",
        }


class UserProfileForm(forms.ModelForm):
    """
    User Profile Form
    ----------------
    Manages user profile information and content preferences.

    Core Fields:
        - profile_image: User's avatar
        - bio: User description
        - country: User location

    Content Preferences:
        - top_movies: Favorite films
        - top_series: Favorite TV shows
        - top_music_albums: Favorite albums
        - top_books: Favorite books
        - top_podcasts: Favorite podcasts
        - top_miscellaneous: Other media preferences
    """

    class Meta:
        model = UserProfile
        fields = [
            "profile_image",
            "bio",
            "country",
            "top_movies",
            "top_series",
            "top_music_albums",
            "top_books",
            "top_podcasts",
            "top_miscellaneous",
        ]
