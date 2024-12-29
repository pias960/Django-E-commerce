

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    full_name = models.CharField(max_length = 30, blank = True, null = True)
    address = models.CharField(max_length = 30, blank = True, null = True)
    country = models.CharField(max_length = 30, blank = True, null = True)
    city = models.CharField(max_length = 30, blank = True, null = True,)
    zip = models.CharField(max_length = 30, blank = True, null = True)
    phone = models.CharField(max_length = 11,  blank = True, null = True,)
    date_joined = models.DateTimeField(auto_now_add = True)
    
    
    



    def __str__(self):
        return f"{self.user.username}s profile"

       
@receiver(post_save, sender=User)
def post_create(sender, instance, created , **kwargs):
        if created:
            Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def post_save(sender,instance, **kwargs):
    instance.profile.save()
    

    
