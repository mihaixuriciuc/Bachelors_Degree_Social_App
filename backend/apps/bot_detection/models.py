from django.db import models
from django.conf import settings


class BotEvent(models.Model):
    """
    this logs suspicious events, when something suspicious happens, the activity is inserted in this table
    """

    class EventType(models.TextChoices):
        THROTTLED = 'THROTTLED', 'Rate limit exceeded'
        FAILED_LOGIN = 'FAILED_LOGIN', 'Failed login attempt'
        RAPID_FOLLOW = 'RAPID_FOLLOW', 'Rapid following'
        REPEATED_COMMENT = 'REPEATED_COMMENT', 'Repeated identical comment'
        SPAM_CONTENT = 'SPAM_CONTENT', 'Spam phrases detected'
        SIGNUP = 'SIGNUP', 'Account created'
        LOGIN = 'LOGIN', 'Successful login'
        SUSPICIOUS_USERNAME = 'SUSPICIOUS_USERNAME', 'Suspicious username'
        USERNAME_CLUSTER = 'USERNAME_CLUSTER', 'Username cluster (bot farm)'
        INCOMPLETE_PROFILE = 'INCOMPLETE_PROFILE', 'Incomplete profile'
        ACTIVITY_BURST = 'ACTIVITY_BURST', 'Activity burst'
        REGULAR_RHYTHM = 'REGULAR_RHYTHM', 'Mechanical timing rhythm'
        DUPLICATE_POSTS = 'DUPLICATE_POSTS', 'Near-duplicate posts'
        DUPLICATE_IMAGE = 'DUPLICATE_IMAGE', 'Reused image across posts'
        DUPLICATE_POST_BURST = 'DUPLICATE_POST_BURST', 'Burst of duplicate posts'
        BOT_NETWORK = 'BOT_NETWORK', 'Dense follow cluster (bot network)'
        ML_SPAM_COMMENT = 'ML_SPAM_COMMENT', 'Spam comments (classifier)'
        ML_SPAM_BIO = 'ML_SPAM_BIO', 'Spam bio (classifier)'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bot_events',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    detail = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        who = self.user.username if self.user else 'anonymous'
        return f"{self.event_type} by {who} at {self.created_at}"


class BlocklistTerm(models.Model):
    """
    """
    term = models.CharField(
        max_length=100,
        unique=True,
        help_text="A substring found in bot usernames (case-insensitive).",
    )
    # Lets you disable a term without deleting it — useful if a term
    # is causing false positives and you want to investigate.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

    class Meta:
        ordering = ['term']


class SpamPhrase(models.Model):
    """
    """
    phrase = models.CharField(
        max_length=200,
        unique=True,
        help_text="A phrase found in spam comments or bios (case-insensitive).",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phrase

    class Meta:
        ordering = ['phrase']