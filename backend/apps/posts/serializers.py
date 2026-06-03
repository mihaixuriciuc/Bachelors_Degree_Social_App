from rest_framework import serializers

from apps.posts.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    # ReadOnlyField with source= pulls a value from a related object
    # without exposing the full foreign key integer.
    author = serializers.ReadOnlyField(source='author.username')

    # SerializerMethodField lets you compute a value with a custom method.
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
        # self.context['request'] is passed in by the ViewSet automatically.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # We check against the prefetched likes queryset (set up in the ViewSet)
            # so this does NOT trigger an extra DB query per post.
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
        # post is set by the ViewSet's perform_create, not by the client.
        # author is read-only (comes from the token).
        # 'post' is intentionally excluded from fields so the client
        # can't pass an arbitrary post_id — the URL param controls that.
        fields = ['id', 'author', 'created_at']