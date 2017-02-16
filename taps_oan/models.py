from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

class Pub(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pub, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Pubs'
    
    def __str__(self):
        return self.name
		
	def __unicode__(self):
	    return self.name

class Beer(models.Model):
    pub = models.ForeignKey(Pub)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):  
        return self.title

	def __unicode__(self):
	    return self.title
		
class UserProfile(models.Model): 
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.user.username