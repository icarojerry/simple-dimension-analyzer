from django.db import models
from analyser.parameters.config import server

class Picture(models.Model):
	id = models.AutoField(primary_key=True)
	file = models.ImageField(blank=False, null=False, upload_to=server['dir_img'])
	distance = models.FloatField(null=True, blank=True, default=-1.0)

	def __str__(self):
		return self.file.name