"""Admin settings"""
from django.contrib import admin

from authenticator.models import AuthGroup, ExternalAuth, Nonce, Association


class AuthGroupOption(admin.ModelAdmin):
    """Auth grouping options"""
    list_display = ('id', 'user', 'email', 'primary')
    search_fields = ('user__name', 'user__email')
    raw_id_fields = ('user',)
    list_select_related = True


class ExternalAuthOption(admin.ModelAdmin):
    """Social Auth user options"""
    list_display = ('id', 'group', 'provider', 'uid')
    search_fields = ('group__user__name', 'group__user__email', 'nickname', 'fullname')
    list_filter = ('provider',)
    raw_id_fields = ('group',)
    list_select_related = True


class NonceOption(admin.ModelAdmin):
    """Nonce options"""
    list_display = ('id', 'server_url', 'timestamp', 'salt')
    search_fields = ('server_url',)


class AssociationOption(admin.ModelAdmin):
    """Association options"""
    list_display = ('id', 'server_url', 'assoc_type')
    list_filter = ('assoc_type',)
    search_fields = ('server_url',)


admin.site.register(AuthGroup, AuthGroupOption)
admin.site.register(ExternalAuth, ExternalAuthOption)
admin.site.register(Nonce, NonceOption)
admin.site.register(Association, AssociationOption)
