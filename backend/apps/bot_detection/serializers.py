from rest_framework import serializers

from apps.user.models import User
from .models import BotEvent


class FlaggedUserSerializer(serializers.ModelSerializer):
    """
    A user row for the flagged-accounts table. Includes the risk score,
    flag status, the breakdown of WHY they were scored, join date, and a
    bit of activity context so the admin can judge at a glance.
    """
    post_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bot_risk_score', 'is_flagged',
            'flag_reasons',                       # the breakdown list
            'date_joined', 'is_active',
            'post_count', 'comment_count', 'follower_count',
        ]

    def get_post_count(self, user):
        return user.posts.count()

    def get_comment_count(self, user):
        return user.comment_set.count()

    def get_follower_count(self, user):
        return user.followers.count()


class BotEventSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    event_label = serializers.CharField(source='get_event_type_display', read_only=True)

    class Meta:
        model = BotEvent
        fields = [
            'id', 'username', 'event_type', 'event_label',
            'ip_address', 'detail', 'created_at',
        ]

    def get_username(self, event):
        return event.user.username if event.user else None