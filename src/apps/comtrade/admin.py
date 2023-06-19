from django.contrib import admin

from apps.comtrade.models import HSCode


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
