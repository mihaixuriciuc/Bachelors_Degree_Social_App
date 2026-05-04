from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user # Only the author can PUT or DELETe



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post_instance = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post_instance)# this takes the user from the token


    def get_queryset(self):
        queryset = Comment.objects.all()

        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')

        # 2. Fetch the actual Post object from the database
        post_instance = get_object_or_404(Post, id=post_id)

        # 3. Save the Like with BOTH the author AND the post attached!
        # 👇 If "post=post_instance" is missing here, you get that IntegrityError! 👇
        serializer.save(author=self.request.user, post=post_instance)
    def get_queryset(self):
        queryset = Like.objects.all()

        post_id = self.kwargs.get('post_pk')
        return Like.objects.filter(post_id=post_id)

    def destroy(self, request, *args, **kwargs):

        post_id = self.kwargs.get('post_pk')

        like_to_delete = Like.objects.filter(post_id=post_id,author=self.request.user)
        if like_to_delete.exists():
            like_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMyPosts(request):
    # Filter posts to only include those created by the logged-in user
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    # We pass the request in the context so the Serializer can calculate 'is_liked'
    serializer = PostSerializer(user_posts, many=True, context={'request': request})
    return Response(serializer.data)