from django.db import models


class HSCode(models.Model):
    """Model for HS codes"""

    id = models.CharField(primary_key=True, editable=False, unique=True)
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.id
