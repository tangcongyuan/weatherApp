from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email_address = models.EmailField(max_length = 100, unique = True)
    location = models.CharField(max_length = 50)
    advertisedDate = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
        return self.email_address
