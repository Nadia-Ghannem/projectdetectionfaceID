from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User  

class UserProfile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)

    face_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length = 100)
    job = models.CharField(max_length = 15)
    phone = models.CharField(max_length =  10)
    email = models.CharField(max_length = 20)
    bio = models.CharField(max_length = 200)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.name