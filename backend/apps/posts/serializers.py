from datetime import timedelta
from django.utils import timezone

from apps.posts.models import Post, Comment, Like
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','author','title','content','created_at','image','likes_count','comments_count','is_liked']

    author = serializers.ReadOnlyField(source='author.username')
    """on this one i have to write a little because im just starting to understand how this works
    the thin is i need to validate that a person cannot make more than 20 posts in one day, for bot spamming reasons
    so i have to get the user who s logged in, i have to request the data
    then i have to define the beggining of the dau 
    
    """
    def validate(self, data):
        # get the data from the authenticated user
        user = self.context['request'].user
        # set a variable with the beggining of the day
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # count how many posts have the timestamp greater or equal with the beggining of the day, if thee are more than 20 then raise error
        #objects is used to use methods for the models
        count = Post.objects.filter(author=user, created_at__gte = today_start).count()

        if count >= 20:
            raise serializers.ValidationError('You cannot post more than 20 posts in one day')
        #i wanted to put here validated data but this happens before is validated, im just learning now its not my fault
        return data

    def get_likes_count(self, post):
        return post.likes.count()
    def get_comments_count(self, post):
        return post.comments.count()

    def get_is_liked(self, obj):
        # Grab the user making the request from the context
        request = self.context.get('request')

        # If they are logged in, check if a Like exists for them on this post
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, author=request.user).exists()

        return False


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'author','content', 'created_at']

    def validate(self, data):
        user = self.context['request'].user

        # set a variable for the time of the comment an hour ago
        hour_beginning = timezone.now() - timedelta(hours=1)

        #count all the cooments left by an user that happened after an hour ago, if there are more than 20 raise error
        count = Comment.objects.filter(author=user, created_at__gte = hour_beginning).count()

        if count >= 20:
            raise serializers.ValidationError('You cannot post more than 20 comments in one day')
        return data


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Like
        fields = ['id','author', 'post_id','created_at']

        read_only_fields = ['post_id']

    def validate(self, data):
        user = self.context['request'].user

        # set a variable for the time of the comment an hour ago
        hour_beginning = timezone.now() - timedelta(hours=1)

        # count all the likes left by an user that happened after an hour ago, if there are more than 20 raise error
        count = Like.objects.filter(author=user, created_at__gte=hour_beginning).count()

        if count >= 300:
            raise serializers.ValidationError('Take a break bro')
        return data






