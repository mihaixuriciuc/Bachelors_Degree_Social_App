from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts import views
from apps.user.views import getMyProfile

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),

    path('profile/', getMyProfile, name='my-profile'),
    path('profile/posts/', views.getMyPosts, name='my-posts'),

    # Any user's posts, by username. Full path: /api/v1/account/users/<username>/posts/
    path('users/<str:username>/posts/', views.getUserPosts, name='user-posts'),

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