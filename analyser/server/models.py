from django.db import models

class Picture(models.Model):
	file = models.ImageField(blank=False, null=False)
	distance = models.DecimalField(null=True, blank=True, default=-1.0,  max_digits=5, decimal_places=2)

	def __str__(self):
		return self.file.name + '| Total Mapped objects:' + str(len(MappedObject.objects.filter(picture=self)))  + ' |' + str(MappedObject.objects.get(picture=self))

class MappedObject(models.Model):
	item_number = models.IntegerField(null=True, blank=True)
	area = models.DecimalField(null=True, blank=True, default=-1.0,  max_digits=5, decimal_places=2)
	picture = models.ForeignKey('Picture', blank=False, on_delete=models.CASCADE)
	file = models.ImageField(blank=True, null=True)

	def __init__(self, *args, **kwargs):
		super(MappedObject, self).__init__(*args, **kwargs)

	def __str__(self):
		return 'Object: ' + str(self.item_number) + " with area = " +  "{:.2f} mm".format(self.area)