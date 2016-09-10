from django.db import models


# Create your models here.


class IngredientName(models.Model):
    primary_id = models.IntegerField()

    name = models.CharField(max_length=500)


class IngredientAmount(models.Model):
    primary_id = models.IntegerField()

    amount = models.IntegerField(default=1)

    units = models.CharField(max_length=100)


class Recipe(models.Model):
    summary = models.CharField(max_length=500)

    plates = models.IntegerField(default=1)

    time = models.CharField(max_length=50, blank=True)

    title = models.CharField(max_length=500, blank=True)

    ingredients = models.ManyToManyField(IngredientAmount)

    link = models.CharField(max_length=500)
