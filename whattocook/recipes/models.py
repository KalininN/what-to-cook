from django.db import models


# Create your models here.

class IngredientNameManager(models.Manager):
	def create_if_not_exists(self, id, name):
		if self.filter(pk=id).exists():
			return
		self.create(pk=id, name=name).save()

class IngredientName(models.Model):
	name = models.CharField(max_length=500)
	objects = IngredientNameManager()
	
	def __str__(self):
		return self.name


class IngredientAmount(models.Model):
	ingredient_id = models.IntegerField()
	amount = models.CharField(max_length=20)
	units = models.CharField(max_length=100)
	
	def __str__(self):
		return u'id=' + str(self.ingredient_id) + u', amount=' + self.amount + self.units


class Recipe(models.Model):
	summary = models.CharField(max_length=500)
	plates = models.IntegerField(default=1)
	time = models.CharField(max_length=50, blank=True)
	title = models.CharField(max_length=500, default='')
	ingredients = models.ManyToManyField(IngredientAmount)
	link = models.CharField(max_length=500)
	
	def __str__(self):
		return self.title

