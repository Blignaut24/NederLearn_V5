from django import forms
from django_summernote.widgets import SummernoteWidget
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
                    "placeholder": "Enter a title for your post..."
                    "(max length 200 characters)",
                    "maxlength": "200",
                }
            ),
            "content": SummernoteWidget(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your blog content here..."
                    "(max length 10000 characters)",
                    "maxlength": "10000",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Write a short excerpt..."
                    "(max length 70 characters)",
                    "maxlength": "70",
                }
            ),
            "media_category": forms.Select(attrs={"class": "form-control"}),
            "release_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0000,
                    "max": datetime.datetime.now().year,
                    "placeholder": "Format YYYY",
                }
            ),
            "media_link": forms.URLInput(attrs={"class": "form-control"}),
        }
        # Hidden labels for cleaner UI
        labels = {
            "blog_title": "Blog Title",
            "content": "Content",
            "excerpt": "Excerpt",
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
            cleaned_data["featured_image"] = "blogpost_placeholder"
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
                    "maxlength": "1000",
                }
            ),
        }
        labels = {"body": ""}


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
        labels = {"profile_image": "Upload Profile Image"}

    widgets = {
        "profile_image": forms.ClearableFileInput(
            attrs={"class": "form-control profile-image-upload"}
        ),
        "bio": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us about yourself "
                "(max length 350 characters)...",
                "maxlength": "350",
            }
        ),
        "country": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Let us know where you are from",
                "maxlength": "70",
            }
        ),
        "top_movies": forms.TextInput(
            attrs={
                "placeholder": "What is your favorite movie?",
                "maxlength": "255",
            }
        ),
        "top_series": forms.TextInput(
            attrs={
                "placeholder": "Series you binge-watched...",
                "maxlength": "255",
            }
        ),
        "top_music_albums": forms.TextInput(
            attrs={
                "placeholder": "Song that make you dance or cry...",
                "maxlength": "255",
            }
        ),
        "top_books": forms.TextInput(
            attrs={
                "placeholder": (
                    "Books that made you laugh so hard "
                    "you dropped them (literally)... 📚💥"
                ),
                "maxlength": "255",
            }
        ),
        "top_podcasts": forms.TextInput(
            attrs={
                "placeholder": "What is your ear candy?",
                "maxlength": "255",
            }
        ),
        "top_miscellaneous": forms.TextInput(
            attrs={
                "placeholder": "Got anything else to share? ",
                "maxlength": "255",
            }
        ),
    }
