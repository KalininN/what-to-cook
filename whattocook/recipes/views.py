import re

from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import transaction

from . import models
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the recipes index.")


def show_recipe(request, recipe_id):
    template = loader.get_template('show_recipe.html')
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


def parse_recipe():
    # -*- coding: utf-8 -*-

    ingredientexpr = re.compile(
        r"<span itemprop=\"ingredient\"[^>]*><[^>]*www\.povarenok\.ru/recipes/ingredient/(\d+)[^>]*>[^>]*>([^<]+)[^>]*>[^>]*>[^>]*>([^<]+)<"
    )

    remscriptsexpr = re.compile(r"<(S|s)cript[^>]*></(S|s)cript>")

    timeexpr = re.compile(r"<time datetime=\"([^\"]+)\"[^>]*>([^<]+)<")

    platesexpr = re.compile(u"<strong>Количество порций:</strong>([^<]+)<")

    summaryexpr = re.compile(r"<span itemprop=\"summary\">([^<]+)<")

    titleexpr = re.compile(r"<h1><[^>]*>([^<]+)<")

    # data = open("index.html", "r", encoding="cp1251").read()
    data = open("index1.html", "r", encoding="cp1251").read()
    data = remscriptsexpr.sub("", data)

    title = titleexpr.search(data).group(1).strip()
    # print(u"title = {}".format(title))

    summary = summaryexpr.search(data).group(1).strip()
    # print(u"summary = {}".format(summary))

    timeneeded = timeexpr.search(data)
    if timeneeded is None:
        timeneeded = ("N/A", "?")
        time = ""
    else:
        timeneeded = (timeneeded.group(1), timeneeded.group(2).strip())
        time = timeneeded[1]
    # print(u"time = {}; value = {}".format(timeneeded[0], timeneeded[1]))

    plates = platesexpr.search(data)
    if plates is None:
        plates = 1
    else:
        plates = plates.group(1).strip()
    # print(u"plates = {}".format(plates))

    with transaction.atomic():
        recipe = models.Recipe(title=title, summary=summary, plates=plates, time=time)
        recipe.save()

        ingredients = ingredientexpr.findall(data)
        for ing in ingredients:
            ingredient_amount = models.IngredientAmount(amount=ing[2], primary_id=ing[0])
            ingredient_amount.save()
            recipe.ingredients.add(ingredient_amount)
            ingredient_name = models.IngredientName(primary_id=ing[0], name=ing[1])
            ingredient_name.save()
            # print(u"id = {}; name = {}; amount = {}".format(ing[0], ing[1], ing[2]))
        recipe.save()
