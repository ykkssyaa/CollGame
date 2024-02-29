from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserForm


class CustomUserAdmin(admin.ModelAdmin):
    form = UserForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('photo',),
        }),
    )


admin.site.register(User, CustomUserAdmin)
