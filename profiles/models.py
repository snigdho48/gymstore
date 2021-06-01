from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone = models.CharField(max_length=15, null=True, blank=True)
    default_billingAdress1 = models.CharField(max_length=250, blank=True)
    default_billingCountry = CountryField(blank_label='Country', null=True, blank=True)  # noqa:501
    default_billingPostcode = models.CharField(max_length=250, blank=True)
    default_billingCity = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()

