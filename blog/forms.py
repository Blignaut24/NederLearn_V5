from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Comment, UserProfile, Blogpost
import datetime


class BlogpostForm(forms.ModelForm):
    """
    # BlogPost Form
    # -------------
    # Handles blog post creation and editing with field validations
    #
    # Key Components:
    #   - Title and content management
    #   - Media metadata collection
    #   - URL validation for external links
    """

    class Meta:
        model = Blogpost
        # Core fields for blog post creation/editing
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

        # Widget configurations with input validations
        widgets = {
            "blog_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter a title for your post...(max length 50 characters)",
                    "maxlength": "50",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your blog content here (max length 2000 characters)...",
                    "maxlength": "2000",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Write a short excerpt...(max length 70 characters)",
                    "maxlength": "70",
                }
            ),
            "media_category": forms.Select(
                attrs={"class": "form-control", "placeholder": "Select Category"}
            ),
            "release_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1800,
                    "max": datetime.datetime.now().year,
                    "placeholder": "Format YYYY",
                    "media_link": forms.URLInput(attrs={"class": "form-control"}),
                }
            ),
        }
        # Hidden labels for cleaner UI
        labels = {
            "blog_title": "Blog Title",
            "content": "Content",
            "excerpt": "Excerpt",
            "status": "Status",
            "featured_image": "Upload Image",
            "media_category": "Media Category",
            "release_year": "Release Year",
            "media_link": "Media Link / Reference",
        }

    def __init__(self, *args, **kwargs):
        super(BlogpostForm, self).__init__(*args, **kwargs)
        self.fields["media_link"].initial = "http://www."

    def clean(self):
        cleaned_data = super().clean()
        featured_image = cleaned_data.get("featured_image")
        if not featured_image:
            cleaned_data["featured_image"] = (
                "blogpost_placeholder"  # default image name
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    """
    # Comment Form
    # -----------
    # Simple form for user comments with character limits
    # Implements responsive design for better UX
    """

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "cols": 50,
                    "placeholder": "Write your comment here...",
                    "max_length": "1000",
                }
            ),
        }
        labels = {
            "body": "",
        }


class UserProfileForm(forms.ModelForm):
    """
    # User Profile Form
    # ----------------
    # Manages user preferences and profile data
    #
    # Features:
    #   - Basic profile information
    #   - Media preferences tracking
    #   - Content categorization
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

        labels = {
            "profile_image": "Upload Profile Image",
        }

    widgets = {
        "profile_image": forms.ClearableFileInput(
            attrs={"class": "form-control profile-image-upload"}
        ),
        "bio": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write something about yourself (max length 350 characters)...",
                "maxlength": "350",
                "country": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "Let us know where you are from",
                        "maxlength": "20",
                    }
                ),
                "top_movies": forms.TextInput(
                    attrs={
                        "placeholder": "Hit us with your absolute favorite movies...",
                        "maxlength": "200",
                    }
                ),
                "top_series": forms.TextInput(
                    attrs={
                        "placeholder": "And series you binge-watched...",
                        "maxlength": "200",
                    }
                ),
                "top_music_albums": forms.TextInput(
                    attrs={
                        "placeholder": "And the albums that make you dance or cry a river...",
                        "maxlength": "200",
                    }
                ),
                "top_books": forms.TextInput(
                    attrs={
                        "placeholder": "Books that you could not let go...",
                        "maxlength": "200",
                    }
                ),
                "top_podcasts": forms.TextInput(
                    attrs={
                        "placeholder": "And not the least, awesome podcasts...",
                        "maxlength": "200",
                    }
                ),
                "top_miscellaneous": forms.TextInput(
                    attrs={
                        "placeholder": "Whatever deserves mentioning like art, festivals, museums etc...",
                        "maxlength": "200",
                    }
                ),
            }
        ),
    }
