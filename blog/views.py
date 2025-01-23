# ===========================================================
# IMPORTS AND DEPENDENCIES
# ===========================================================
# Django Core
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView
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


# ===========================================================
# BLOG POST CREATION
# ===========================================================
class BlogpostCreateView(CreateView):
    """Handle creation of new blog posts with author attribution"""

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# =============================================================================
# BASE VIEWS
# =============================================================================
def index(request):
    """Base view for rendering the main landing page."""
    return render(request, "index.html")


# =============================================================================
# BLOG MANAGEMENT
# =============================================================================
class BlogpostPostList(generic.ListView):
    """
    List View: Displays all blog posts

    Features:
    - Pagination (6 posts per page)
    - Filtered by active status
    - Ordered by creation date
    - Requires authentication
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """Authentication check before displaying content."""
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


class BlogPostDetail(View):
    """
    Detail View: Individual blog post handling

    Features:
    - Display single post
    - Comment management
    - Like status tracking
    """

    def get(self, request, slug, *args, **kwargs):
        """
        GET: Retrieve and display blog post details

        Args:
            slug (str): Unique post identifier
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
        POST: Handle comment submission

        Args:
            slug (str): Unique post identifier
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
# INTERACTION FEATURES
# =============================================================================
class LikeUnlike(View):
    """
    Like Management: Toggle like status on posts

    Features:
    - Add/remove likes
    - User-specific tracking
    """

    def post(self, request, slug, *args, **kwargs):
        """
        Toggle like status for current user

        Args:
            slug (str): Post identifier
        """
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# =============================================================================
# USER PROFILE MANAGEMENT
# =============================================================================
class ProfileView(View):
    """Display current user's profile information"""

    def get(self, request):
        """Fetch and show logged-in user's profile"""
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """Display other users' profile information"""

    def get(self, request, username):
        """
        Fetch and show requested user's profile

        Args:
            username (str): Target user's username
        """
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Profile Editor: Handle profile updates

    Features:
    - Form-based editing
    - File upload support
    - Authentication required
    """

    def get(self, request):
        """Display profile edit form"""
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        """Process profile updates"""
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})
