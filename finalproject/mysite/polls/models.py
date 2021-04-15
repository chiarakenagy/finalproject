import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def _str_(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #many to one model
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def _str_(self):
        return self.choice_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #one to one model
    location = models.CharField(max_length=100)
