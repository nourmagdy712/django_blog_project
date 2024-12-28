from rest_framework import serializers
from .models import BlogPost, Category, Tag
from django.contrib.auth.models import User

# Serializer for User registration.
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is not exposed in the response
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

# Serializer for BlogPost model.
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags', [])  # If no tags, use an empty list
        # Get the Category instance by name
        category = Category.objects.get(name=category_data)
        # Handle tags: Fetch tags based on the list of tag names
        tags = [Tag.objects.get(name=tag_name) for tag_name in tags_data]
        blog_post = BlogPost.objects.create(category=category, **validated_data)
        blog_post.tags.set(tags)
        return blog_post
# Serializer for Category model.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Serializer for Tag model.
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']