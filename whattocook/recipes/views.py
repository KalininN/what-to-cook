from django.shortcuts import render
from django.template import loader

# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the recipes index.")


def showrecipe(request, recipe_id):
	template = loader.get_template('showrecipe.html')
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	context = {
		"id": recipe_id,
		"recipe": recipe,
		"ingredients": []
	}
	for ing_amount in recipe.ingredients.all():
		ing = IngredientName.objects.get(primary_id=ing_amount.primary_id)
		context["ingredients"].append({"name": ing.name, "amount": str(ing_amount.amount) + " " + ing_amount.units})
	return HttpResponse(template.render(context, request))
