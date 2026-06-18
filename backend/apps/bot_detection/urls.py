from django.urls import path

from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
    path('flagged/', views.flagged_users, name='flagged-users'),
    path('events/', views.recent_events, name='recent-events'),
    path('recompute/', views.recompute_scores, name='recompute-scores'),
    path('clear-flag/<int:user_id>/', views.clear_flag, name='clear-flag'),
]