from django.db import models


# Create your models here.


class IngredientName(models.Model):
    primary_id = models.IntegerField()

    name = models.CharField(max_length=500)


class IngredientAmount(models.Model):
    primary_id = models.IntegerField()

    amount = models.IntegerField()

    units = models.CharField()


class Recipe(models.Model):
    summary = models.CharField(max_length=500)

    plates = models.IntegerField(default=1)

    time = models.IntegerField(blank=True)

    title = models.CharField(max_length=500)

    ingredients = models.ManyToManyField(IngredientAmount)
