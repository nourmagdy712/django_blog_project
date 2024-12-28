from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import BlogPost, Category, Tag
from .serializers import BlogPostSerializer, TagSerializer, UserRegistrationSerializer
from .pagination import BlogPostPagination  
from django.views.generic import View
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# from django.shortcuts import get_object_or_404
# from rest_framework import generics 
# from rest_framework.permissions import IsAuthenticated , IsAdminUser , IsAuthenticatedOrReadOnly

class UserRegistrationView(APIView):
    # Handle user registration.
    
    def post(self, request):
        # Extract data from the request
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    # Handle user login.
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):

    # Handle user logout.
    
    def post(self, request):
        logout(request)  # Log the user out
        return Response({"detail": "User logged out successfully"}, status=status.HTTP_200_OK)
    
class BlogPostViewSet(viewsets.ModelViewSet):

    # ViewSet for managing blog posts.

    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['category', 'author', 'tags', 'published_date']  # Optional: Add filter options for category, author, etc.
    ordering_fields = ['published_date', 'category', 'created_date']  # Fields to sort by
    ordering = ['-published_date']  # Default sorting (descending order of published date)

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        blog_post = self.get_object()
        if blog_post.author != request.user:
            return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        blog_post = self.get_object()
        if blog_post.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class BlogPostSearchView(APIView):

     """
    Search blog posts by title, content, tags, or author.
    """

     def get(self, request):
        query = request.query_params.get('q', None)  # Search query for title, content, author, tags
        category = request.query_params.get('category', None)
        author = request.query_params.get('author', None)
        tags = request.query_params.get('tags', None)  # Optional tags filter

        posts = BlogPost.objects.all()

        # Search by title, content, and author
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            )

        # Filter by category (optional)
        if category:
            posts = posts.filter(category__name__icontains=category)

        # Filter by author (optional)
        if author:
            posts = posts.filter(author__username=author)

        # Filter by tags (optional) - this filters blog posts with specific tags
        if tags:
            tag_list = tags.split(',')  # Assume tags are passed as a comma-separated list (e.g., 'django,python')
            posts = posts.filter(tags__name__in=tag_list).distinct()

        # Paginate the queryset
        paginator = BlogPostPagination()
        result_page = paginator.paginate_queryset(posts, request)
        if result_page is not None:
            serializer = BlogPostSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no pagination is needed (i.e., return all results), serialize the data
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class TagListView(ListAPIView):

    # List all tags.
   
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(RetrieveAPIView):
   
    # Retrieve a specific tag by ID.
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BlogPostDeleteView(View):
    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Delete request received successfully.'})