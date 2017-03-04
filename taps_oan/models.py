from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

from yelpapi import YelpAPI


class YelpSearch(models.Model):
    client_id = 'dWTg7AOcL3n4FiY5PoUQBQ'
    client_secret = 'ZGXA8JWlX10i9PeI9a0kJZ0lFYNFaWYQYjNhXTcMzEo7pp0F3UiaMot6kMPh109M'
    yelp_api = YelpAPI(client_id, client_secret)
    search_results = yelp_api.search_query(term='bar', location='Glasgow', limit=50)


class Beer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return "/taps_oan/beer/%s/" % self.slug

    def save(self, *args, **kwargs):
        setattr(self, 'name', self.name.title())
        self.slug = slugify(self.name)
        super(Beer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __unicode__(self):
            return self.name


class Pub(models.Model):
    name = models.CharField(max_length=128, unique=True)
    beers = models.ManyToManyField(Beer, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return "/taps_oan/pub/%s/" % self.slug

    def save(self, *args, **kwargs):
        setattr(self, 'name', self.name.title())
        self.slug = slugify(self.name)
        super(Pub, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Pubs'

    def __str__(self):
        return self.name

    def __unicode__(self):
            return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username
