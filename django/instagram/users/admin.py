# Librerias
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile

# Poder registrar un usuario desde el panel administrativo
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('pk', 'user', 'telefono', 'foto')
	list_display_links = ('pk', 'user',)
	list_editable = ('telefono', 'foto')
	search_fields = ('user__email', 'user__first_name', 'user__last_name', 'telefono')
	list_filter = ('created', 'modified', 'user__is_active', 'user__is_staff')

	fieldsets = (
		('Profile', {
			'fields': ('user', 'foto'),
		}),
		('Extra Info', {
			'fields': (('telefono'), ('biografia')),
		}),
		('Metadata', {
			'fields': ('created', 'modified'),
		}),
	)

	readonly_fields = ('created', 'modified')

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)