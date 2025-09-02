# from django.contrib import admin

# Register your models here.
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PractitionerProfile

class PractitionerProfileInline(admin.StackedInline):
    model = PractitionerProfile
    can_delete = False
    verbose_name_plural = 'Practitioner Profile'
    fk_name = 'user'

# Extend the default User admin to include the profile inline
class UserAdmin(BaseUserAdmin):
    inlines = (PractitionerProfileInline,)

# unregister the original User and re-register with the new admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Also register the PractitionerProfile on its own (optional)
@admin.register(PractitionerProfile)
class PractitionerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'service_location', 'phone_number', 'id_number', 'created_at')
    search_fields = ('user__username','user__email','id_number','phone_number')
