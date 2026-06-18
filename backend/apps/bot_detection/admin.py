from django.contrib import admin
from .models import BotEvent, BlocklistTerm, SpamPhrase


@admin.register(BotEvent)
class BotEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'ip_address', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'event_type', 'detail', 'created_at')


@admin.register(BlocklistTerm)
class BlocklistTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('term',)


@admin.register(SpamPhrase)
class SpamPhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('phrase',)