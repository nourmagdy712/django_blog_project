from . import views
from django.urls import path, include
from .views import BlogPostViewSet, TagListView, TagDetailView, BlogPostSearchView, BlogPostDeleteView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)
#Automatically creates the necessary CRUD routes for BlogPost, GET /api/posts/: To view all blog posts& POST /api/posts/: To create a new blog post (authenticated users only).

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),

     # Search functionality
    path('posts/search/', BlogPostSearchView.as_view(), name='post-search'),
    #Delete post
    path('posts/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    # Tag URLs
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),

    # Include the BlogPost routes (using the DefaultRouter)
    path('', include(router.urls)),

    # path('posts/', BlogList.as_view(), name='create_blog_post'),
    # path('posts/<int:id>/', BlogList.as_view(), name='retrieve_blog_post'),
]