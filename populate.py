import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'project.settings')

import django
import random

django.setup()
from taps_oan.models import Beer, Pub


def populate():
    # First, we will create lists of dictionaries containing the beers
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    arbitrary_beers = [
        {"name": "Budweiser",
         "views": "1"},
        {"name": "Tennents",
         "views": "2"},
        {"name": "Coors Light",
         "views": "4"},
        {"name": "West",
         "views": "8"},
        {"name": "Guinness",
         "views": "10"},
        {"name": "Stella Artois",
         "views": "13"},
        {"name": "Carling",
         "views": "17"},
        {"name": "Carlsberg",
         "views": "22"},
        {"name": "Heineken",
         "views": "26"},
        {"name": "Staropramen",
         "views": "29"},
        {"name": "Brooklyn Lager",
         "views": "33"},
        {"name": "John Smith",
         "views": "41"},
        {"name": "Strongbow",
         "views": "54"}]

    arbitrary_pubs = [
        {"name": "Brewdog Glasgow",
         "views": "1"},
        {"name": "The Mallard",
         "views": "2"},
        {"name": "Bar Soba",
         "views": "4"},
        {"name": "Oran Mor",
         "views": "8"},
        {"name": "The Crafty Pig",
         "views": "12"},
        {"name": "Coopers",
         "views": "17"},
        {"name": "Hillhead Bookclub",
         "views": "23"}]

    for beer in arbitrary_beers:
        add_beer(beer["name"], beer["views"])

    for pub in arbitrary_pubs:
        p = add_pub(pub["name"], pub["views"])
        for b in Beer.objects.all():
            if (random.randint(0, 10) < 5):
                p.beers.add(b)

    for check_pub in Pub.objects.all():
        for check_beer in check_pub.beers.all():
            print("- {0} - {1}".format(str(check_pub), str(check_beer)))


            
def add_pub(name, views):
    p = Pub.objects.get_or_create(name=name)[0]
    p.views = views
    p.save()
    return p


def add_beer(name, views):
    b = Beer.objects.get_or_create(name=name)[0]
    b.views = views
    b.save()
    return b


if __name__ == '__main__':
    populate()
