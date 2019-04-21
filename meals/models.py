from django.db import models

class Menu(models.Model):
    day = models.CharField(max_length = 20)
    menu = models.CharField(max_length = 500)
    

    objects = models.Manager()  # VSC Bug : has no objects members 수정방법
    def __str__(self):
        return self.day


