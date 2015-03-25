from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#this is our manin, topic model. 
class Topic(models.Model):
        name = models.CharField(max_length=128, unique=True)
        slug = models.SlugField(unique=True)
        likecount = models.IntegerField(default=0)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Topic, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Lesson(models.Model):
    topic = models.ForeignKey(Topic)
    title = models.CharField(max_length=128)
    url = models.URLField()

    def __unicode__(self):      
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username