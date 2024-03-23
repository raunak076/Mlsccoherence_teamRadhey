from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.name
    
class context(models.Model):
    email = models.CharField(max_length=128)
    contextText = models.CharField(max_length=1024)
    def __str__(self):
        return self.email+"-"+self.contextText

