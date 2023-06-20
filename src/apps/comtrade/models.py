from django.db import models


class HSCode(models.Model):
    """Model for HS codes"""

    id = models.CharField(primary_key=True, editable=False, unique=True)
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.id


class Country(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    name = models.TextField(max_length=255, blank=True)
    iso_alpha3_code = models.CharField(max_length=3, blank=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
