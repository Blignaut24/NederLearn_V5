# Import required Django modules and views
from . import views
from django.urls import path

# URL pattern definitions
urlpatterns = [
    # Home route
    # GET / - Display list of all blog posts
    path("", views.BlogpostPostList.as_view(), name="home"),
    
    # Individual post route
    # GET /<slug> - Show detailed view of specific post
    path('<slug:slug>/', views.BlogPostDetail.as_view(), name='blogpost_detail'),
    
    # Post interaction route
    # POST /like/<slug> - Handle like/unlike actions
    path('like/<slug:slug>/', views.LikeUnlike.as_view(), name='like_unlike'),
]