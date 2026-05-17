from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Post, Comment, Like
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .throttling import (
    PostCreationThrottle,
    CommentCreationThrottle,
    LikeCreationThrottle,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Post.objects.prefetch_related('likes', 'comments').order_by('-created_at')

    def get_throttles(self):
        # Only throttle creation, not reads or updates.
        # get_throttles() is called by DRF before the view runs.
        # It returns a list of throttle instances; DRF checks each one.
        # If any returns False, the request gets a 429 response.
        if self.action == 'create':
            return [PostCreationThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def get_throttles(self):
        if self.action == 'create':
            return [CommentCreationThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post_instance = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post_instance)


class LikeViewSet(viewsets.ModelViewSet):
    """
    Likes only support three actions: list, create, and destroy.

    PUT and PATCH are meaningless for a like — there's nothing to update.
    Exposing them violates the Interface Segregation Principle: the client
    sees methods that make no sense for this resource.

    We restrict the allowed actions here, and the urls.py only registers
    the matching HTTP methods.
    """
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    # http_method_names controls which HTTP verbs the ViewSet responds to.
    # This is the simplest way to block PUT/PATCH without writing custom logic.
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Like.objects.filter(post_id=post_id)

    def get_throttles(self):
        if self.action == 'create':
            return [LikeCreationThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post_instance = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post_instance)

    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_pk')
        like_to_delete = Like.objects.filter(post_id=post_id, author=request.user)

        if like_to_delete.exists():
            like_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "You haven't liked this post."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMyPosts(request):
    user_posts = Post.objects.filter(author=request.user).prefetch_related('likes', 'comments')
    serializer = PostSerializer(user_posts, many=True, context={'request': request})
    return Response(serializer.data)