from django.contrib import admin
from django.apps import apps
from .import models

class CreateInputAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.CreateInput._meta.fields if field.name != "id"]

class GlobalResultsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.GlobalResults._meta.fields if field.name != "id"]

admin.site.register(models.CreateInput, CreateInputAdmin)
admin.site.register(models.GlobalResults, GlobalResultsAdmin)
