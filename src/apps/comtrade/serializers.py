from rest_framework import serializers

from apps.comtrade import models


class HSCodeSerializer(serializers.ModelSerializer):
    """Serializer to validate HS codes"""

    class Meta:
        model = models.HSCode
        fields = ("id", "description")


class CountrySerializer(serializers.ModelSerializer):
    """Serializer to validate HS codes"""

    class Meta:
        model = models.Country
        fields = ("id", "name", "iso_alpha3_code")
