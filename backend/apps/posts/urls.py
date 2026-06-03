from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts import views
from apps.user.views import getMyProfile

router = DefaultRouter()
# basename= is required because PostViewSet overrides get_queryset()
# instead of setting queryset= as a class attribute. The router needs
# a name to generate URL names like 'post-list' and 'post-detail'.
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),

    path('profile/', getMyProfile, name='my-profile'),
    path('profile/posts/', views.getMyPosts, name='my-posts'),

    # Comments support full CRUD: you can list, create, update, and delete comments.
    path(
        'posts/<int:post_pk>/comments/',
        views.CommentViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='comment-list',
    ),

    # Likes only support list, create, and delete.
    # PUT and PATCH are removed — updating a like is meaningless.
    path(
        'posts/<int:post_pk>/likes/',
        views.LikeViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
        }),
        name='like-list',
    ),
]