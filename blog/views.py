# ===========================================================================
# Django Blog Application - Core Views and Models
# ===========================================================================
# Author: [Your Name]
# Created: 2024-01-24
# Description: Main application views for blog functionality including CRUD
#              operations, user profiles, and content management
# ===========================================================================

# -----------------------------
# Core Dependencies
# -----------------------------
# Django standard imports
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Authentication modules
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Local app imports
from .models import Blogpost, UserProfile
from .forms import CommentForm, UserProfileForm, BlogpostForm


# -----------------------------
# Blog Post CRUD Operations
# -----------------------------
class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """Create new blog posts with author attribution"""

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Update existing blog posts while maintaining author info"""

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
    """Handle blog post deletion with confirmation"""

    model = Blogpost
    template_name = "blogpost_delete.html"
    success_url = reverse_lazy("my_posts")


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """Display user's personal blog posts with pagination"""

    model = Blogpost
    template_name = "my_posts.html"
    context_object_name = "my_blogposts"
    paginate_by = 6

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user).order_by("-created_on")


# -----------------------------
# Core Application Views
# -----------------------------
def index(request):
    """Render the main landing page"""
    return render(request, "index.html")


# -----------------------------
# Content Display Views
# -----------------------------
class BlogpostPostList(generic.ListView):
    """
    Main blog listing with pagination and filtering
    - Shows only active posts
    - Orders by creation date
    - Requires authentication
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


class BlogPostDetail(View):
    """
    Single post view with comments and interactions
    Handles both GET (display) and POST (comment) requests
    """

    def get(self, request, slug, *args, **kwargs):
        """Display post content and related data"""
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
        """Process new comment submissions"""
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
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": comment_form,
            },
        )


# -----------------------------
# User Interaction Features
# -----------------------------
class LikeUnlike(View):
    """Toggle post likes for authenticated users"""

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# -----------------------------
# User Profile Management
# -----------------------------
class ProfileView(View):
    """View user's own profile data"""

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """View other users' profile information"""

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """Handle profile updates and image uploads"""

    def get(self, request):
        """Display edit form"""
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        """Process form submission"""
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})
