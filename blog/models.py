# =================================================================
# IMPORTS AND CONFIGURATIONS
# =================================================================
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# =======================================
# Create Models Here
# =======================================

# Constants for post status
STATUS = ((0, "Draft"), (1, "Published"))

# =================================================================
# PRIMARY MODEL: Blog Post
# =================================================================
# Purpose: Stores blog posts with user interactions and media info


class Blogpost(models.Model):
    """
    Stores blog posts with user interactions and media info
    """

    # Core Fields
    # -----------
    blog_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # Timestamps
    # ----------
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Content
    # -------
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    featured_image = CloudinaryField("image", default="placeholder")

    # Media Details
    # ------------
    media_category = models.ForeignKey('MediaCategory', on_delete=models.SET_NULL, related_name='blog_posts', blank=True, null=True) # Temporarily disabled required field validation - will be re-enabled in future update

    release_year = models.IntegerField()
    media_link = models.URLField()

    # User Engagement
    # --------------
    likes = models.ManyToManyField(User, related_name="blogpost_likes", blank=True)
    bookmarks = models.ManyToManyField(
        User, related_name="blogpost_bookmarks", blank=True
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        """Returns the blog title as string representation"""
        return self.blog_title

    def number_of_likes(self):
        """Returns the total number of likes"""
        return self.likes.count()

    def number_of_bookmarks(self):
        """Returns the total number of bookmarks"""
        return self.bookmarks.count()


# =================================================================
# SUPPORTING MODEL: Media Category
# =================================================================
# Purpose: Groups content by media type (e.g. movies, books) to organize blog posts.
class MediaCategory(models.Model):
    """
    A way to group different types of content like movies and books. This helps organize     blog posts based on what type of media they're about.
    """

    media_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Returns the media category name as string representation"""
        return self.media_name

    class Meta:
        verbose_name_plural = "Media Categories"


# =================================================================
# USER PROFILE MODEL
# =================================================================
# Purpose: Adds extra features to the basic Django user profile, letting users save their favorite media and customize their profile details.


class UserProfile(models.Model):
    """
    This model adds extra features to regular user accounts, letting people share th  eir favorite media and personal details.
    """

    # Core User Data
    # -------------
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField("image", default="placeholder")
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Media Preferences
    # ----------------
    # All fields are optional (blank=True) and store user's favorite content
    top_movies = models.CharField(max_length=255, blank=True)
    top_series = models.CharField(max_length=255, blank=True)
    top_music_albums = models.CharField(max_length=255, blank=True)
    top_books = models.CharField(max_length=255, blank=True)
    top_podcasts = models.CharField(max_length=255, blank=True)
    top_miscellaneous = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """Returns username as string representation"""
        return self.user.username


# =================================================================
# COMMENTS
# =================================================================
# Purpose: A model that enables users to comment on blog posts, with a moderation system for approving comments before they appear


class Comment(models.Model):
    """
    Lets users leave comments on posts and requires approval before they show up
    """

    # Comment content and metadata
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # Relationships
    blogpost = models.ForeignKey('Blogpost', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment {self.body} by {self.user.username}"
