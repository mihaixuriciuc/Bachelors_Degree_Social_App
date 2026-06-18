

from datetime import timedelta

from django.utils import timezone
from django.db.models import Count

from apps.user.models import User, Follow
from . import constants
import statistics
from apps.posts.models import Comment, Post, Like
from .models import BotEvent, BlocklistTerm, SpamPhrase
import re


def _username_stem(username: str) -> str:
    # Strip trailing digits first.
    stem = re.sub(r'\d+$', '', username)
    # Then strip any trailing separator left behind (_ - .)
    stem = re.sub(r'[._-]+$', '', stem)
    return stem


def _levenshtein_distance(s1: str, s2: str) -> int:

    m = len(s1)
    n = len(s2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string.
    for j in range(n + 1):
        dp[0][j] = j   # j insertions needed
    for i in range(m + 1):
        dp[i][0] = i   # i deletions needed

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],       # delete from s1
                    dp[i][j - 1],       # insert into s1
                    dp[i - 1][j - 1],   # substitute
                )

    return dp[m][n]


class BotDetectionEngine:


    @staticmethod
    def check_username_pattern(user):
        username = user.username
        if not username:
            return 0, None

        digit_count = sum(c.isdigit() for c in username)
        digit_ratio = digit_count / len(username)

        trailing = 0
        for c in reversed(username):
            if c.isdigit():
                trailing += 1
            else:
                break

        if (
            digit_ratio >= constants.USERNAME_DIGIT_RATIO
            or trailing >= constants.USERNAME_TRAILING_DIGITS
        ):
            return constants.POINTS['username_pattern'], "Username looks auto-generated"
        return 0, None

    @staticmethod
    def check_username_blocklist(user):
        """
        Username contains a known bot-associated substring.
        Terms are stored in the BlocklistTerm table — editable from the admin
        without touching code. Only active terms are checked.
        """
        lowered = user.username.lower()

        # Fetch all active terms from the DB. This is one query per recompute
        # per user, but the table is small so it's fast. If performance ever
        # became a concern, you'd cache this list for the duration of a
        # recompute_all() call.
        active_terms = BlocklistTerm.objects.filter(is_active=True).values_list(
            'term', flat=True
        )

        for term in active_terms:
            if term.lower() in lowered:
                return (
                    constants.POINTS['username_blocklist'],
                    f"Username contains blocklisted term '{term}'",
                )
        return 0, None


    @staticmethod
    def check_shared_ip(user):

        user_ips = (
            BotEvent.objects
            .filter(user=user)
            .exclude(ip_address__isnull=True)
            .values_list('ip_address', flat=True)
            .distinct()
        )

        for ip in user_ips:
            distinct_users = (
                BotEvent.objects
                .filter(ip_address=ip)
                .values('user')
                .distinct()
                .count()
            )
            if distinct_users >= constants.SHARED_IP_THRESHOLD:
                return constants.POINTS['shared_ip'], f"IP {ip} shared by {distinct_users} accounts"
        return 0, None

    @staticmethod
    def check_throttle_events(user):

        count = BotEvent.objects.filter(
            user=user,
            event_type=BotEvent.EventType.THROTTLED,
        ).count()

        if count == 0:
            return 0, None

        points = min(
            count * constants.POINTS['throttle_event'],
            constants.THROTTLE_EVENT_CAP,
        )
        return points, f"Hit rate limits {count} times"

    @staticmethod
    def check_failed_logins(user):
        count = BotEvent.objects.filter(
            event_type=BotEvent.EventType.FAILED_LOGIN,
            detail__icontains=f"attempted username: {user.username}",
        ).count()

        if count == 0:
            return 0, None

        points = min(
            count * constants.POINTS['failed_login'],
            constants.FAILED_LOGIN_CAP,
        )
        return points, f"{count} failed login attempts"

    @staticmethod
    def check_repeated_comments(user):
        repeated = (
            Comment.objects
            .filter(author=user)
            .values('content')
            .annotate(n=Count('id'))
            .filter(n__gte=constants.REPEATED_COMMENT_THRESHOLD)
        )

        if repeated.exists():
            worst = max(row['n'] for row in repeated)
            return constants.POINTS['repeated_comment'], f"Posted the same comment {worst} times"
        return 0, None

    @staticmethod
    def check_spam_phrases(user):
        """
        A user's comments or bio contain known spam phrases.
        Phrases are stored in the SpamPhrase table — editable from the admin.
        We check both comments AND the bio here, since both are natural-language
        text where spam phrasing is equally suspicious.
        """
        active_phrases = list(
            SpamPhrase.objects.filter(is_active=True).values_list('phrase', flat=True)
        )

        if not active_phrases:
            return 0, None

        # Check comments.
        comments = Comment.objects.filter(author=user).values_list('content', flat=True)
        for content in comments:
            lowered = content.lower()
            for phrase in active_phrases:
                if phrase.lower() in lowered:
                    return (
                        constants.POINTS['spam_phrase'],
                        f"Comment contains spam phrase '{phrase}'",
                    )

        # Check bio — same classifier, different text surface.
        try:
            bio = user.profile.bio
            if bio:
                lowered_bio = bio.lower()
                for phrase in active_phrases:
                    if phrase.lower() in lowered_bio:
                        return (
                            constants.POINTS['spam_phrase'],
                            f"Bio contains spam phrase '{phrase}'",
                        )
        except Exception:
            pass

        return 0, None
    @staticmethod
    def check_follow_velocity(user):
        window_start = timezone.now() - timedelta(
            minutes=constants.FOLLOW_VELOCITY_WINDOW_MINUTES
        )
        recent_follows = Follow.objects.filter(
            follower=user,
            created_at__gte=window_start,
        ).count()

        if recent_follows >= constants.FOLLOW_VELOCITY_THRESHOLD:
            return (
                constants.POINTS['follow_velocity'],
                f"Followed {recent_follows} accounts in the last "
                f"{constants.FOLLOW_VELOCITY_WINDOW_MINUTES} minutes",
            )
        return 0, None

    @staticmethod
    def check_profile_completeness(user):

        try:
            profile = user.profile
        except Exception:
            return constants.POINTS['incomplete_profile'], "No profile"

        has_pic = bool(profile.profile_pic)
        has_bio = bool(profile.bio and profile.bio.strip())

        if not has_pic and not has_bio:
            return constants.POINTS['incomplete_profile'], "No picture and no bio"
        return 0, None

    @staticmethod
    def check_activity_burst(user):
        window_start = timezone.now() - timedelta(
            minutes=constants.ACTIVITY_BURST_WINDOW_MINUTES
        )

        posts = Post.objects.filter(
            author=user, created_at__gte=window_start
        ).count()
        comments = Comment.objects.filter(
            author=user, created_at__gte=window_start
        ).count()
        likes = Like.objects.filter(
            author=user, created_at__gte=window_start
        ).count()
        follows = Follow.objects.filter(
            follower=user, created_at__gte=window_start
        ).count()

        total_actions = posts + comments + likes + follows

        if total_actions >= constants.ACTIVITY_BURST_THRESHOLD:
            return (
                constants.POINTS['activity_burst'],
                f"{total_actions} actions in "
                f"{constants.ACTIVITY_BURST_WINDOW_MINUTES} minutes "
                f"({posts} posts, {comments} comments, {likes} likes, {follows} follows)",
            )
        return 0, None

    @staticmethod
    def check_regular_rhythm(user):
        window_start = timezone.now() - timedelta(hours=constants.RHYTHM_WINDOW_HOURS)

        timestamps = []
        timestamps += list(
            Post.objects.filter(author=user, created_at__gte=window_start)
            .values_list('created_at', flat=True)
        )
        timestamps += list(
            Comment.objects.filter(author=user, created_at__gte=window_start)
            .values_list('created_at', flat=True)
        )
        timestamps += list(
            Like.objects.filter(author=user, created_at__gte=window_start)
            .values_list('created_at', flat=True)
        )
        timestamps += list(
            Follow.objects.filter(follower=user, created_at__gte=window_start)
            .values_list('created_at', flat=True)
        )


        if len(timestamps) < constants.RHYTHM_MIN_ACTIONS:
            return 0, None


        timestamps.sort()

        gaps = [
            (timestamps[i] - timestamps[i - 1]).total_seconds()
            for i in range(1, len(timestamps))
        ]

        avg_gap = statistics.mean(gaps)
        gap_stddev = statistics.stdev(gaps)

        if (
                gap_stddev < constants.RHYTHM_STDDEV_THRESHOLD
                and avg_gap <= constants.RHYTHM_MAX_AVG_GAP_SECONDS
        ):
            return (
                constants.POINTS['regular_rhythm'],
                f"Machine-like timing: {len(timestamps)} actions evenly spaced "
                f"~{avg_gap:.0f}s apart (variation {gap_stddev:.1f}s)",
            )
        return 0, None

    @staticmethod
    def check_username_cluster(user):
        """
        Detects bot farms whose usernames share the same stem after stripping
        trailing digits. e.g. target_0 ... target_24 all reduce to 'target'.

        This is the fast, cheap first pass. The fuzzy check below catches
        the harder cases where the stem itself is slightly varied.
        """
        stem = _username_stem(user.username)

        # If nothing was stripped, the name has no numeric suffix
        # and can't form a digit-based cluster.
        if stem == user.username or not stem:
            return 0, None

        candidates = User.objects.filter(
            username__startswith=stem
        ).values_list('username', flat=True)

        cluster_size = sum(
            1 for name in candidates
            if _username_stem(name) == stem
        )

        if cluster_size >= constants.USERNAME_CLUSTER_THRESHOLD:
            return (
                constants.POINTS['username_cluster'],
                f"Username part of a cluster of {cluster_size} "
                f"similar names ('{stem}...')",
            )
        return 0, None

    @staticmethod
    def check_fuzzy_username_cluster(user):
        """
        Catches bot farms whose usernames are similar but not identical —
        close enough to be clearly related, different enough to slip past
        the exact-stem cluster check.

        Uses Levenshtein distance to compare this username against all others.
        If many accounts are within CLUSTER_FUZZY_DISTANCE edits, they were
        likely created in a batch.

        Performance note: O(n) per user — fine at this scale. In production
        you'd use an indexed stem column to narrow candidates first.
        """
        username = user.username.lower()

        if len(username) < constants.CLUSTER_MIN_STEM_LENGTH:
            return 0, None

        all_usernames = (
            User.objects
            .exclude(pk=user.pk)
            .values_list('username', flat=True)
        )

        similar_count = 0
        for other in all_usernames:
            other_lower = other.lower()
            if len(other_lower) < constants.CLUSTER_MIN_STEM_LENGTH:
                continue
            distance = _levenshtein_distance(username, other_lower)
            if distance <= constants.CLUSTER_FUZZY_DISTANCE:
                similar_count += 1

        if similar_count >= constants.USERNAME_CLUSTER_THRESHOLD:
            return (
                constants.POINTS['fuzzy_cluster'],
                f"Username is edit-distance-close to {similar_count} "
                f"other accounts (possible bot farm)",
            )
        return 0, None

    CHECKS = [
        check_username_pattern,
        check_username_blocklist,
        check_shared_ip,
        check_throttle_events,
        check_failed_logins,
        check_repeated_comments,
        check_spam_phrases,
        check_follow_velocity,
        check_profile_completeness,
        check_activity_burst,
        check_regular_rhythm,
        check_username_cluster,
        check_fuzzy_username_cluster,
    ]

    @staticmethod
    def recompute_user(user):
        total = 0
        reasons = []

        for check in BotDetectionEngine.CHECKS:
            points, reason = check.__func__(user)
            if points > 0:
                total += points
                reasons.append({"reason": reason, "points": points})

        user.bot_risk_score = total
        user.is_flagged = total >= constants.FLAG_THRESHOLD
        user.flag_reasons = reasons
        user.save(update_fields=['bot_risk_score', 'is_flagged', 'flag_reasons'])

        return {
            "username": user.username,
            "score": total,
            "is_flagged": user.is_flagged,
            "reasons": reasons,
        }

    @staticmethod
    def recompute_all():
        results = []
        users = User.objects.filter(is_staff=False).select_related('profile')

        for user in users:
            results.append(BotDetectionEngine.recompute_user(user))

        flagged = [r for r in results if r["is_flagged"]]
        return {
            "total_scanned": len(results),
            "total_flagged": len(flagged),
            "results": results,
        }

