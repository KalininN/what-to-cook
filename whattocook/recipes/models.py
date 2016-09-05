from django.db import models

# Create your models here.


class Recipe(models.Model):
	summary = models.CharField(max_length=500)
	plates = models.IntegerField(default=1)
