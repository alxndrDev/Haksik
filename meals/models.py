from django.db import models

class Menu(models.Model):
    day = models.CharField(max_length = 20)
    menu = models.CharField(max_length = 500)
