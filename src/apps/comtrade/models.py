from django.db import models
from django.core.validators import MinValueValidator


class HSCode(models.Model):
    """Model for HS codes"""

    id = models.CharField(
        primary_key=True, editable=False, unique=True, max_length=10
    )
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.id


class Region(models.Model):
    """Class for Regions"""

    id = models.CharField(
        primary_key=True, editable=False, unique=True, max_length=255
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name.capitalize()


class Country(models.Model):
    """Class for Countries"""

    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    name = models.TextField(max_length=255, blank=True)
    iso_alpha3_code = models.CharField(max_length=3, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class SingletonModel(models.Model):
    """Class to create single object model"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SkipDay(SingletonModel):
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(2)], default=2
    )

    def __str__(self):
        return f"Skipped {self.amount} days"
