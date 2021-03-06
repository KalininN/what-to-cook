# -*- coding: utf-8 -*-

import re
import requests

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils import timezone

from .models import *


def index(request):
    template = loader.get_template('titlepage.html')
    context = {'last_recipes': Recipe.objects.order_by('add_time').all()[:5]}
    return HttpResponse(template.render(context, request))


def parse_amount(amount_units):
    words = amount_units.split()
    if not words:
        return -1, ''
    if len(words) == 1:
        return -1, words[0]
    try:
        words[0] = int(words[0])
    except ValueError:
        return -1, ' '.join(words)
    return words[0], ' '.join(words[1:])


@require_POST
def addrecipe_post(request):
    recipe_id = request.POST['id']
    try:
        recipe_id = int(recipe_id)
    except ValueError:
        return HttpResponseBadRequest()

    if Recipe.objects.filter(pk=recipe_id).exists():
        return HttpResponseRedirect(reverse('recipes:showrecipe', args=(recipe_id,)))

    ingredientexpr = re.compile(
        r"<span itemprop=\"ingredient\"[^>]*><[^>]*www\.povarenok\.ru/recipes/ingredient/(\d+)[^>]*>[^>]*>([^<]+)[^>]*>[^>]*>[^>]*>([^<]+)<")
    remscriptsexpr = re.compile(r"<(S|s)cript[^>]*></(S|s)cript>")
    timeexpr = re.compile(r"<time datetime=\"([^\"]+)\"[^>]*>([^<]+)<")
    platesexpr = re.compile(u"<strong>Количество порций:</strong>([^<]+)<")
    summaryexpr = re.compile(r"<span itemprop=\"summary\">([^<]+)<")
    titleexpr = re.compile(r"<h1><[^>]*>([^<]+)<")

    req = requests.get(r'http://www.povarenok.ru/recipes/show/' + str(recipe_id) + r'/')
    if req.status_code != requests.codes.ok:
        return HttpResponseBadRequest()
    data = req.text
    data = remscriptsexpr.sub("", data)

    title = titleexpr.search(data).group(1).strip()

    summary = summaryexpr.search(data).group(1).strip()

    timeneeded = timeexpr.search(data)
    if timeneeded is None:
        #timeneeded = ("N/A", "?")
        time = ""
    else:
        timeneeded = (timeneeded.group(1), timeneeded.group(2).strip())
        time = timeneeded[1]

    plates = platesexpr.search(data)
    if plates is None:
        plates = 1
    else:
        plates = plates.group(1).strip()

    with transaction.atomic():
        recipe = Recipe(id=recipe_id, title=title, summary=summary, plates=plates, time=time, add_time=timezone.now())
        recipe.save()

        ingredients = ingredientexpr.findall(data)
        for ing in ingredients:
            ing_amount, ing_units = parse_amount(ing[2])
            print('amount = {}, units = {}'.format(ing_amount, ing_units))
            ingredient_amount = IngredientAmount(amount=ing_amount, units=ing_units, ingredient_id=ing[0])
            ingredient_amount.save()
            recipe.ingredients.add(ingredient_amount)
            IngredientName.objects.create_if_not_exists(ing[0], ing[1])
        recipe.save()
    return HttpResponseRedirect(reverse('recipes:showrecipe', args=(recipe_id,)))


def addrecipe_get(request):
    template = loader.get_template('addrecipe.html')
    return HttpResponse(template.render({}, request))


def addrecipe(request):
    if request.method == 'POST':
        return addrecipe_post(request)
    else:
        return addrecipe_get(request)


def showrecipe(request, recipe_id):
    template = loader.get_template('showrecipe.html')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        "id": recipe_id,
        "recipe": recipe,
        "ingredients": []
    }
    for ing_amount in recipe.ingredients.all():
        ing = IngredientName.objects.get(pk=ing_amount.ingredient_id)
        context["ingredients"].append({"name": ing.name, "amount": str(ing_amount.amount) + " " + ing_amount.units})
        if ing_amount.amount == -1:
            context["ingredients"][-1]["amount"] = ing_amount.units
    return HttpResponse(template.render(context, request))
