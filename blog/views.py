# ===========================================================================
# Django Blog Application - Core Views
# ===========================================================================
# Purpose: Core views and models for blog functionality
# Features: CRUD operations, user profiles, content management
# ===========================================================================

# -----------------------------
# Import Section
# -----------------------------
# Django core
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

# Authentication
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Local imports
from .models import Blogpost, UserProfile, MediaCategory
from .forms import CommentForm, UserProfileForm, BlogpostForm


# -----------------------------
# Blog Post CRUD Views
# -----------------------------
class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Creates new blog posts

    Args:
        LoginRequiredMixin: Ensures user authentication
        generic.CreateView: Base view for creation

    Returns:
        Redirects to post detail view on success
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Updates existing blog posts

    Args:
        LoginRequiredMixin: Ensures user authentication
        generic.UpdateView: Base view for updates

    Returns:
        Redirects to post detail view on success
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_update.html"
    success_url = reverse_lazy("blogpost_detail")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Handles post deletion

    Args:
        LoginRequiredMixin: Ensures user authentication
        generic.DeleteView: Base view for deletion

    Returns:
        Redirects to user's posts on success
    """

    model = Blogpost
    template_name = "blogpost_delete.html"
    success_url = reverse_lazy("my_posts")


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """
    Lists user's personal posts

    Args:
        LoginRequiredMixin: Ensures user authentication
        ListView: Base view for list display

    Returns:
        Paginated list of user's posts
    """

    model = Blogpost
    template_name = "my_posts.html"
    context_object_name = "my_blogposts"
    paginate_by = 6

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user).order_by("-created_on")


# -----------------------------
# Core Views
# -----------------------------
def index(request):
    """Renders main landing page"""
    return render(request, "index.html")


# -----------------------------
# Content Display Views
# -----------------------------
class BlogpostPostList(generic.ListView):
    """
    Main blog listing view

    Features:
        - Shows active posts only
        - Orders by newest first
        - Requires authentication
        - Includes pagination
    """

    model = Blogpost
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


def get_queryset(self):
    queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
    media_category = self.request.GET.get("category")
    if media_category:
        queryset = queryset.filter(media_category__media_name=media_category)
    return queryset


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Lägg till kategorier i kontexten för att visa i mallen
    context["categories"] = MediaCategory.objects.all()
    # Lägg till övriga relevanta data i kontexten
    return context


class BlogPostDetail(View):
    """
    Handles single post display and comments

    Methods:
        get: Shows post content and comments
        post: Processes new comment submissions
    """

    def get(self, request, slug, *args, **kwargs):
        """
        Displays post details

        Args:
            slug: Post identifier

        Returns:
            Rendered template with post data
        """
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = blogpost.likes.filter(id=self.request.user.id).exists()

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
        Processes comment submission

        Args:
            slug: Post identifier

        Returns:
            Rendered template with updated comments
        """
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = blogpost.likes.filter(id=request.user.id).exists()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()

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


# -----------------------------
# User Interaction Views
# -----------------------------
class LikeUnlike(View):
    """
    Handles post like/unlike toggling

    Methods:
        post: Toggles like status and redirects
    """

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# -----------------------------
# Profile Management Views
# -----------------------------
class ProfileView(View):
    """
    Shows user's own profile data

    Methods:
        get: Displays profile information
    """

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """
    Displays other users' profiles

    Methods:
        get: Shows public profile data
    """

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Handles profile updates

    Methods:
        get: Shows edit form
        post: Processes profile updates
    """

    def get(self, request):
        """Displays edit form"""
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        """Processes form submission"""
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles account deletion

    Features:
        - Requires authentication
        - Confirms user ownership
        - Handles logout after deletion
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


def bookmarked(request):
    if request.user.is_authenticated:
        bookmarked_posts = Blogpost.objects.filter(bookmarks=request.user)
    else:
        bookmarked_posts = []
    return render(request, "bookmarked.html", {"bookmarked_posts": bookmarked_posts})


class BookmarkUnbookmark(View):
    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.bookmarks.filter(id=request.user.id).exists():
            blogpost.bookmarks.remove(request.user)
        else:
            blogpost.bookmarks.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))
