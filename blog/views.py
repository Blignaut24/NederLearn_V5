# =============================================================================
# IMPORTS & DEPENDENCIES
# =============================================================================
"""
Core Django imports for routing and view handling
Authentication modules for user management
Local imports for models and forms
"""
# Django Core
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Authentication
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Local imports
from .models import Blogpost, UserProfile
from .forms import CommentForm, UserProfileForm, BlogpostForm


# =============================================================================
# BLOG POST CRUD OPERATIONS
# =============================================================================
"""
Create, Read, Update, Delete views for blog posts
All views require authentication
"""


class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """Creates new blog posts and assigns current user as author"""

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Handles updates to existing blog posts"""

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
    """Manages blog post deletion with confirmation"""

    model = Blogpost
    template_name = "blogpost_confirm_delete.html"
    success_url = reverse_lazy("home")


# =============================================================================
# BASE VIEWS
# =============================================================================
"""Main landing page and core navigation views"""


def index(request):
    """Renders the main landing page"""
    return render(request, "index.html")


# =============================================================================
# BLOG LIST & DETAIL VIEWS
# =============================================================================
"""
Primary views for displaying blog content
Includes list view with pagination and detailed post view
"""


class BlogpostPostList(generic.ListView):
    """
    Displays paginated list of active blog posts
    - 6 posts per page
    - Filtered by active status
    - Chronological order
    - Auth required
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """Ensures user authentication before access"""
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


class BlogPostDetail(View):
    """
    Detailed view of individual blog posts
    Handles both display and comment submission
    """

    def get(self, request, slug, *args, **kwargs):
        """Displays post details and related content"""
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
        """Processes new comment submissions"""
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


# =============================================================================
# USER INTERACTIONS
# =============================================================================
"""Handles user interactions like likes and comments"""


class LikeUnlike(View):
    """Toggles like status for authenticated users"""

    def post(self, request, slug, *args, **kwargs):
        """Switches like status and redirects to post"""
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# =============================================================================
# USER PROFILE MANAGEMENT
# =============================================================================
"""
Profile views and management
Includes viewing own profile, other users' profiles, and profile editing
"""


class ProfileView(View):
    """Shows current user's profile"""

    def get(self, request):
        """Fetches and displays user profile"""
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """Displays other users' profiles"""

    def get(self, request, username):
        """Fetches and shows requested user profile"""
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Handles profile updates and image uploads
    Requires authentication
    """

    def get(self, request):
        """Shows profile edit form"""
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        """Processes profile updates"""
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})
