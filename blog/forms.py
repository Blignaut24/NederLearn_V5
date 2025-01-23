from .models import Comment, UserProfile
from django import forms


class CommentForm(forms.ModelForm):
    """
        This is a form that handles user comments.

    It includes:
    • A space for writing comments
    • Rules for how comments should look
    • Settings for the comment box
    """

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 2,  # Height of text area
                    "cols": 50,  # Width of text area
                    "placeholder": "Drop your thoughts here like they're hot! 🔥",  # Default text
                    "max_length": "1500",  # Maximum characters
                }
            ),
        }
        labels = {
            "body": "",
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for managing user profile information.

    Fields:
        - Profile image
        - Bio
        - Country
        - Favorite content preferences:
            * Movies
            * TV Series
            * Music
            * Books
            * Podcasts
            * Misc items
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
