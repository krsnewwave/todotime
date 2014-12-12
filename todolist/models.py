import datetime
from django.db import models
from django.contrib.auth.models import User

#
# class User(models.Model):
# username = models.CharField(max_length=20)
# password = models.CharField(max_length=20)
#     full_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=250)


class Note(models.Model):
    text = models.CharField(max_length=1000)
    date_posted = models.DateTimeField('date posted', default=datetime.datetime.now())
    date_due = models.DateTimeField('due date')
    is_cancelled = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.text