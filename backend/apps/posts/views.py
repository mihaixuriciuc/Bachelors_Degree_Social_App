from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user # Only the author can PUT or DELETe



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)# this takes the user from the token


    def get_queryset(self):
        queryset = Comment.objects.all()

        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Like.objects.all()

        post_id = self.kwargs.get('post_pk')
        return Like.objects.filter(post_id=post_id)
