from .models import Comment
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
