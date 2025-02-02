# Standard Django and third-party imports
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Global variables
current_year = timezone.now().year


# Validation Functions
def validate_year(value):
    """
    Validates if a year is within acceptable range (1800 to current year)

    Args:
        value (int): Year to validate

    Raises:
        ValidationError: If year is outside acceptable range
    """
    current_year = timezone.now().year
    if not (1800 <= value <= current_year):
        raise ValidationError(
            _("Please enter a year between 1800 and %(current_year)s"),
            params={"current_year": current_year},
        )


# Constants
STATUS = ((0, "Draft"), (1, "Published"))


# Models
class MediaCategory(models.Model):
    """
    Stores categories for media content

    Fields:
        media_name (CharField): Unique identifier for media category
    """

    media_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.media_name

    class Meta:
        verbose_name_plural = "Media Categories"


class UserProfile(models.Model):
    """
    Extended user profile information

    Fields:
        user (OneToOneField): Link to Django User model
        profile_image (CloudinaryField): User's profile picture
        bio (TextField): User biography
        country (CharField): User's location
        top_* (CharField): User's favorite media in different categories
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField("image", default="placeholder")
    bio = models.TextField(max_length=350, blank=True)
    country = models.CharField(max_length=150, blank=True)
    top_movies = models.CharField(max_length=255, blank=True)
    top_series = models.CharField(max_length=255, blank=True)
    top_music_albums = models.CharField(max_length=255, blank=True)
    top_books = models.CharField(max_length=255, blank=True)
    top_podcasts = models.CharField(max_length=255, blank=True)
    top_miscellaneous = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Blogpost(models.Model):
    """
    Main blog post content model

    Fields:
        blog_title (CharField): Post title
        slug (SlugField): URL-friendly title
        author (ForeignKey): Post creator
        content (TextField): Main post content
        status (IntegerField): Draft or Published
        media_* (Various): Associated media information

    Methods:
        save(): Handles slug generation and image defaults
        number_of_*(): Count likes and bookmarks
    """

    blog_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=10000)
    excerpt = models.TextField(max_length=150, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    featured_image = CloudinaryField("image", default="blogpost_placeholder")
    media_category = models.ForeignKey(
        "MediaCategory",
        on_delete=models.SET_NULL,
        related_name="blog_posts",
        null=True,
        blank=False,
    )
    release_year = models.IntegerField(validators=[validate_year])
    media_link = models.URLField()
    likes = models.ManyToManyField(
        User, related_name="blogpost_likes", blank=True
    )
    bookmarks = models.ManyToManyField(
        User, related_name="blogpost_bookmarks", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_title)
        if not self.featured_image:
            self.featured_image = "blogpost_placeholder"
        super(Blogpost, self).save(*args, **kwargs)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_bookmarks(self):
        return self.bookmarks.count()


class Comment(models.Model):
    """
    User comments on blog posts

    Fields:
        body (TextField): Comment content
        created_on (DateTimeField): Timestamp
        approved (BooleanField): Moderation status
        blogpost (ForeignKey): Associated blog post
        user (ForeignKey): Comment author
    """

    body = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    blogpost = models.ForeignKey(
        "Blogpost", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} by {self.user.username}"
