from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from brokers.models import Exchange 
from brokers.models import Tariff 
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    passport_data = models.CharField(max_length=20, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    exchanges = models.ManyToManyField(Exchange, blank=True)
    def __str__(self):
        return self.username
    
class UserTariff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'exchange')
    
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     passport_data = models.CharField(max_length=20, blank=True)
#     balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"Профиль {self.user.username}"
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()