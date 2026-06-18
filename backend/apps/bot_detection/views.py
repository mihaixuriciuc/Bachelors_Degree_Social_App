from datetime import timedelta

from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.user.models import User
from .models import BotEvent
from .serializers import FlaggedUserSerializer, BotEventSerializer
from .detection import BotDetectionEngine


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):

    now = timezone.now()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)

    events_today = BotEvent.objects.filter(created_at__gte=day_ago).count()
    events_week = BotEvent.objects.filter(created_at__gte=week_ago).count()
    by_type = list(
        BotEvent.objects
        .values('event_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    flagged_count = User.objects.filter(is_flagged=True).count()
    total_users = User.objects.filter(is_staff=False).count()

    return Response({
        "flagged_count": flagged_count,
        "total_users": total_users,
        "events_today": events_today,
        "events_week": events_week,
        "events_by_type": by_type,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def flagged_users(request):
    show_all = request.query_params.get('all') == 'true'

    qs = User.objects.filter(is_staff=False)
    if not show_all:
        qs = qs.filter(is_flagged=True)

    qs = qs.order_by('-bot_risk_score', '-date_joined')

    serializer = FlaggedUserSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def recent_events(request):
    events = BotEvent.objects.select_related('user')[:50]
    serializer = BotEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def recompute_scores(request):
    summary = BotDetectionEngine.recompute_all()
    return Response({
        "message": "Scores recomputed.",
        "total_scanned": summary["total_scanned"],
        "total_flagged": summary["total_flagged"],
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_flag(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_flagged = False
    user.bot_risk_score = 0
    user.save(update_fields=['is_flagged', 'bot_risk_score','flag_reasons'])

    return Response({
        "message": f"Flag cleared for {user.username}.",
    })