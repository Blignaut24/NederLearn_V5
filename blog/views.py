################################################################
# IMPORTS
################################################################

# Django Core Components
# - HTTP Response handlers and authentication
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# - URL handling and view utilities
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator

# Django View Components
# - Generic view classes and messaging
from django.views import generic, View
from django.views.generic import DeleteView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Application Models and Forms
# - Custom models and form classes for blog functionality
from .models import Blogpost, UserProfile, MediaCategory
from .forms import CommentForm, UserProfileForm, BlogpostForm

# =================================================================
# BlogpostCreateView - Handles creation of new blog posts
# =================================================================
# Inherits from:
# - LoginRequiredMixin: Ensures user authentication
# - generic.CreateView: Provides base create view functionality


class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating new blog posts

    Attributes:
        model: Database model for blog posts
        form_class: Form for handling blog post data
        template_name: Template for rendering create view
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        """
        Process valid form submission

        Args:
            form: Validated form instance

        Returns:
            HTTP response after successful creation
        """
        # Set current user as post author
        form.instance.author = self.request.user

        # Save form and get response
        response = super().form_valid(form)

        # Add success message
        messages.success(
            self.request, "Your blog post has been created successfully."
        )
        return response

    def get_success_url(self):
        """
        Define redirect URL after successful post creation

        Returns:
            URL to detail view of newly created post
        """
        return reverse_lazy(
            "blogpost_detail", kwargs={"slug": self.object.slug}
        )


# ------------------------------------------------------------------------------
# BlogpostUpdateView - Handles updating existing blog posts
# ------------------------------------------------------------------------------
# Inherits:
#   - LoginRequiredMixin: Ensures user authentication
#   - generic.UpdateView: Provides update functionality
# ------------------------------------------------------------------------------


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Manages the updating of existing blog posts.

    Requirements:
        - User must be authenticated
        - User can only edit their own posts
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_update.html"

    def form_valid(self, form):
        """
        Validates and processes the form submission.

        Steps:
        1. Sets current user as post author
        2. Saves the form
        3. Displays success message
        """
        form.instance.author = self.request.user  # Ensure correct authorship
        response = super().form_valid(form)
        messages.success(
            self.request, "Your blog post has been updated successfully."
        )
        return response

    def get_success_url(self):
        """Returns URL to redirect to after successful update"""
        return reverse_lazy(
            "blogpost_detail", kwargs={"slug": self.object.slug}
        )

    def get_queryset(self):
        """
        Restricts access to posts owned by current user only.
        Security measure to prevent unauthorized edits.
        """
        return Blogpost.objects.filter(author=self.request.user)


# ------------------------------------------------------
# BlogpostDeleteView - Handles deletion of blog posts
# ------------------------------------------------------
# Inherits:
#   - LoginRequiredMixin: Ensures user authentication
#   - generic.DeleteView: Provides delete functionality
# ------------------------------------------------------

class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Manages the deletion of existing blog posts.

    Requirements:
        - User must be logged in
        - User can only delete their own posts
    """

    model = Blogpost
    template_name = "blogpost_delete.html"
    success_url = reverse_lazy(
        "my_posts"
    )  # Redirect after successful deletion

    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add success message
        Returns: HTTP response after deletion
        """
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request, "Your blog post has been deleted successfully."
        )
        return response

    def get_queryset(self):
        """
        Security filter to ensure users can only delete their own posts
        Returns: QuerySet filtered by current user
        """
        return Blogpost.objects.filter(author=self.request.user)


# ===================================================
# Blog Post Views - User Posts & List Views
# ===================================================


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """
    Displays posts created by logged-in user.

    Attributes:
        model: Blogpost model
        template: my_posts.html template
        context: 'my_blogposts' for template access
        pagination: 6 posts per page
    """

    model = Blogpost
    template_name = "my_posts.html"
    context_object_name = "my_blogposts"
    paginate_by = 6

    def get_queryset(self):
        # Filter posts by current user, newest first
        return Blogpost.objects.filter(author=self.request.user).order_by(
            "-created_on"
        )


class BlogPostList(generic.ListView):
    """
    Main blog post listing view.

    Features:
    - Shows all published posts
    - Supports category filtering
    - Requires user authentication
    - Paginates results

    Attributes:
        model: Blogpost model
        template: index.html template
        context: 'blogposts' for template access
        pagination: 6 posts per page
    """

    model = Blogpost
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """
        Authentication check before view execution.
        Redirects to login if user not authenticated.
        """
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Get published posts, newest first
        queryset = Blogpost.objects.filter(status=1).order_by("-created_on")

        # Apply category filter if specified
        media_category = self.request.GET.get("category")
        if media_category:
            queryset = queryset.filter(
                media_category__media_name=media_category
            )
        return queryset

    def get_context_data(self, **kwargs):
        # Add categories for template filtering
        context = super().get_context_data(**kwargs)
        context["categories"] = MediaCategory.objects.all()
        return context


# ------------------------------------------------------------------------------
# BlogPostDetail View
# ------------------------------------------------------------------------------
# Purpose: Handles displaying and commenting on individual blog posts
# Methods: GET (display post), POST (handle comments)
# ------------------------------------------------------------------------------


class BlogPostDetail(View):
    """
    Displays individual blog post details and handles comment submissions.

    Key functionality:
    - Shows post content, comments, and like status
    - Processes new comment submissions
    - Manages comment form state
    """

    def get(self, request, slug, *args, **kwargs):
        # Get published blog post or 404
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)

        # Get unapproved comments in chronological order
        comments = blogpost.comments.filter(approved=False).order_by(
            "created_on"
        )

        # Check if user has liked the post
        liked = False
        if blogpost.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Render template with context
        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Handles comment submission on a blog post

        Flow:
        1. Get blog post and existing comments
        2. Validate and save new comment
        3. Reset form if valid
        4. Re-render template with updated context
        """
        # Get post and comment data
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by(
            "created_on"
        )
        liked = blogpost.likes.filter(id=request.user.id).exists()

        # Process comment form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()  # Reset form after successful save

        # Render updated template
        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": comment_form.is_valid(),
                "liked": liked,
                "comment_form": comment_form,
            },
        )


# ==========================================
# LIKE/UNLIKE FUNCTIONALITY
# ==========================================


class LikeUnlike(View):
    """
    Handles post like/unlike toggling

    Methods:
        post: Toggle like status for authenticated user
    """

    def post(self, request, slug, *args, **kwargs):
        # Get blog post or 404
        blogpost = get_object_or_404(Blogpost, slug=slug)

        # Toggle like status
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)  # Unlike
        else:
            blogpost.likes.add(request.user)  # Like

        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# ==========================================
# PROFILE VIEWS
# ==========================================


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    """
    Display logged-in user's profile

    Methods:
        get: Render user profile page
    """

    def get(self, request):
        # Get user profile data
        user_profile = get_object_or_404(UserProfile, user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(LoginRequiredMixin, View):
    """
    Display other user's profile

    Methods:
        get: Render profile page for specified username
    """

    def get(self, request, username):
        # Get requested user's profile
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)

        # Set context with profile ownership check
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Edit user profile functionality

    Methods:
        get: Display profile edit form
        post: Handle form submission and update
    """

    def get(self, request):
        # Load existing profile into form
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        # Get profile and process form data
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )

        # Validate and save form
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully."
            )
            return redirect("profile")

        return render(request, "profile_edit.html", {"form": form})


# -------------------------------
# Account Management Views
# -------------------------------


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles user account deletion

    Requires:
    - User must be logged in
    - Only allows users to delete their own account

    Flow:
    1. Verifies user authentication
    2. Deletes user account
    3. Logs out user
    4. Redirects to login page
    """

    model = User
    template_name = "account_manage.html"
    success_url = reverse_lazy("account_login")

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response


# -------------------------------
# Bookmark Management Views
# -------------------------------


def bookmarked(request):
    """
    Displays user's bookmarked posts

    Logic:
    - If user is authenticated: Shows their bookmarked posts
    - If not authenticated: Returns empty list

    Returns:
    - Renders bookmarked.html with list of bookmarked posts
    """
    if request.user.is_authenticated:
        bookmarked_posts = Blogpost.objects.filter(bookmarks=request.user)
    else:
        bookmarked_posts = []

    return render(
        request, "bookmarked.html", {"bookmarked_posts": bookmarked_posts}
    )


class BookmarkUnbookmark(View):
    """
    Toggles bookmark status for posts

    Actions:
    - If post is bookmarked: Removes bookmark
    - If post isn't bookmarked: Adds bookmark

    Flow:
    1. Gets blog post by slug
    2. Checks current bookmark status
    3. Toggles bookmark status
    4. Shows success message
    5. Redirects to post detail page
    """

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.bookmarks.filter(id=request.user.id).exists():
            blogpost.bookmarks.remove(request.user)
            messages.success(request, "Removed from 'Bookmarked'.")
        else:
            blogpost.bookmarks.add(request.user)
            messages.success(request, "Added to 'Bookmarked'.")
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# ============================================================================
# ERROR HANDLERS
# ============================================================================
# Provides custom error pages for specific HTTP error responses
# Improves user experience by showing friendly error messages
# Supports 403 (Forbidden) and 405 (Method Not Allowed) errors
# ============================================================================


def custom_403_error(request, exception):
    """
    Handles 403 Forbidden errors with custom error page

    Parameters:
        request: Django request object
        exception: Error that triggered this handler

    Returns:
        Rendered 403.html template as HttpResponseForbidden
    """
    return HttpResponseForbidden(render(request, "403.html"))


def custom_405_error(request, exception):
    """
    Handles 405 Method Not Allowed errors with custom error page

    Parameters:
        request: Django request object
        exception: Error that triggered this handler

    Returns:
        Rendered 405.html template as HttpResponseNotAllowed
    """
    return HttpResponseNotAllowed(render(request, "405.html"))
