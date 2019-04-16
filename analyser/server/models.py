from django.db import models
from .models import Picture

class Picture(models.Model):
	id = models.AutoField(primary_key=True)
    file = models.ImageField(blank=False, null=False)
    distance = models.FloatField(null=True, blank=True, default=-1.0)
    def __str__(self):
        return self.file.name