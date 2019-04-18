from django.db import models

class Picture(models.Model):
	file = models.ImageField(blank=False, null=False)
	distance = models.FloatField(null=True, blank=True, default=-1.0)
	

	def __str__(self):
		return self.file.name

class MappedObject(models.Model):
	area = models.FloatField(null=True, blank=True, default=-1.0)
	picture = models.ForeignKey('Picture', blank=False, on_delete=models.CASCADE)