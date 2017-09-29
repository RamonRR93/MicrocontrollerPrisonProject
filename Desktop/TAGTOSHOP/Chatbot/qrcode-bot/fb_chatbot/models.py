from __future__ import unicode_literals
from django.db import models


# Create your models here.
class FacebookUser(models.Model):
    fb_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_pic = models.CharField(max_length=255)
    locale = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    has_fb_data = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name

class QRCode(models.Model):
    style = models.CharField(max_length=255, default="Text")
    url = models.CharField(max_length=255)
    data = models.CharField(max_length=255)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Scan(models.Model):
    fbuser = models.ForeignKey(FacebookUser, db_index=False)
    qrcode = models.ForeignKey(QRCode, db_index=False)
    date = models.DateTimeField(auto_now=True)
