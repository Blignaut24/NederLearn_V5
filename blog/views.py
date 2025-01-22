# Standard Django imports
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Blogpost
from .forms import CommentForm


# Basic index view
def index(request):
    """Render the main index page"""
    return render(request, "index.html")


# =================================================================
# Blog List View
# =================================================================
class BlogpostPostList(generic.ListView):
    """
    Displays paginated blog posts (6 per page) sorted by creation date using the Blogpost model.
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """
        The system requires authentication to view pages.
        Unauthenticated users are redirected to login before accessing content.
        """
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


# =================================================================
# Blog Detail View
# =================================================================
class BlogPostDetail(View):
    """Shows blog posts and lets users add comments"""

    def get(self, request, slug, *args, **kwargs):
        """
        GET: Displays the blog post, including all comments and whether the user has liked it

        Input:
            slug: The unique ID of the blog post
        Output:
            Shows the blog post page to the u
        """
        # Fetch post and related data
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
        POST method: Handles new comments on a blog post

        Args:
            slug: The blog post's unique ID
        Returns:
            Shows the page with the comment's updateus
        """
        # Fetch post data
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = blogpost.likes.filter(id=request.user.id).exists()

        # Process comment form
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


# =================================================================
# Like/Unlike Functionality
# =================================================================
class LikeUnlike(View):
    """Add or remove likes on blog posts"""

    def post(self, request, slug, *args, **kwargs):
        """
        Changes whether a user likes or unlikes a post

        Arguments:
            slug: Unique ID for the blog post
        Returns:
            Goes back to the post page
        """
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))
