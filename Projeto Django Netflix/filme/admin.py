from django.contrib import admin
from .models import Filme, Episodio, Serie, Usuario
from django.contrib.auth.admin import UserAdmin

new_campo = list(UserAdmin.fieldsets)

new_campo.append(
    ("Histórico", {"fields": ("filmes_assistidos",)})
)
UserAdmin.fieldsets = tuple(new_campo)

# Register your models here.

admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Serie)
admin.site.register(Usuario, UserAdmin)
