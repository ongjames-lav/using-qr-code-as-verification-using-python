from django.contrib import admin
from .models import User, QRCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('date_joined',)

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_valid', 'last_used')
    list_filter = ('is_valid', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'last_used', 'qr_code')
    fields = ('user', 'is_valid', 'qr_code', 'created_at', 'last_used')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # Only generate QR code when creating new record
            super().save_model(request, obj, form, change)
        else:
            # When editing, only update is_valid field
            obj.save(update_fields=['is_valid'] if 'is_valid' in form.changed_data else None)
