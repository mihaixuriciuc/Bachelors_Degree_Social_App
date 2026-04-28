from django.urls import path,include


from rest_framework.routers import DefaultRouter

from apps.posts import views
from apps.posts.views import CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    path('',include(router.urls)),

    path('posts/<int:post_pk>/comments/',CommentViewSet.as_view(
        {'get':'list','post':'create','put':'update','patch':'partial_update','delete':'destroy'}),
    name='comment-list'),

    path('posts/<int:post_pk>/likes/',LikeViewSet.as_view(
        {'get':'list','post':'create','put':'update','patch':'partial_update','delete':'destroy'}),
          name='like-list'
         )

]