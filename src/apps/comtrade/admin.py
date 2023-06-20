from django.contrib import admin

from apps.comtrade.models import HSCode, Country


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "description")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "iso_alpha3_code")
