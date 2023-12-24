from tkinter import CASCADE
from turtle import mode
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Images(models.Model):
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(auto_now_add=True)
    is_last_landscape = True
    # added_by = models.ForeignKey(get_user_model(), on_delete=CASCADE)
