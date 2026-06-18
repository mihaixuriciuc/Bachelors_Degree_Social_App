from rest_framework import serializers

from apps.posts.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content',
            'created_at', 'image',
            'likes_count', 'comments_count', 'is_liked',
        ]

    def get_likes_count(self, post):
        return post.likes.count()

    def get_comments_count(self, post):
        return post.comments.count()

    def get_is_liked(self, post):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return post.likes.filter(author=request.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = ['id', 'author', 'created_at']