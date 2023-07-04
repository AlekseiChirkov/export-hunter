from django.contrib import admin

from apps.comtrade.models import HSCode, Region, Country, SkipDay


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "description")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "iso_alpha3_code")


@admin.register(SkipDay)
class SkipDaysAdmin(admin.ModelAdmin):
    list_display = ("amount", )
