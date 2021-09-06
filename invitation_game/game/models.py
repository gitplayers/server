from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.db.models.fields import CharField
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from pathlib import Path
import json

script_location = Path(__file__).absolute().parent
file_location = script_location / 'static/game/character_map.json'
file_location2 = script_location / 'static/game/questions.json'

with file_location.open() as json_file:
    characterData = json.load(json_file)
   
def character_list_tuple(data):
    lista = []
    for value in data:
        lista.append((value['id'], value['title']))
    return lista

# def question_conversor(data):

#     return lista

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=100)
    incorret_answers = ArrayField(
        models.CharField(max_length=100, blank=True),
        size=3,
    )
    class Meta:
        verbose_name_plural = "questions"

class Character(models.Model):
    name = models.CharField(max_length=100)
    hair_id = models.IntegerField(choices=character_list_tuple(characterData['hair']))
    skin_id = models.IntegerField(choices=character_list_tuple(characterData['skin']))
    dress_id = models.IntegerField(choices=character_list_tuple(characterData['dress']))
    eyes_id = models.IntegerField(choices=character_list_tuple(characterData['eyes']))
    
    class Meta:
        verbose_name_plural = "characters"

class Score(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

    class Meta:
        verbose_name_plural = "scores"

class Invitation(models.Model):
    title = models.CharField(max_length=300)
    message = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "invitations"

class Game(models.Model):
    date =  models.DateField(default=timezone.now)
    questions = models.ManyToManyField(Question, blank=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    scores = models.ManyToManyField(Score, blank=True)

    class Meta:
        verbose_name_plural = "games"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wedding_url= models.CharField(max_length=30, blank=True, null=True)
    side1 = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='side1', blank=True, null=True)
    side2 = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='side2', blank=True, null=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        print(instance.is_superuser)
        if created and not instance.is_superuser:
           Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if not instance.is_superuser:
            instance.profile.save()