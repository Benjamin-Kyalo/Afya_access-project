# from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class PractitionerProfile(models.Model):
    class Designation(models.TextChoices):
        DOCTOR = 'doctor', _('Doctor')
        NURSE = 'nurse', _('Nurse')
        LAB = 'lab', _('Lab Tech')
        PHARMACIST = 'pharmacist', _('Pharmacist')
        OTHER = 'other', _('Other')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='practitionerprofile')
    id_number = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=30, choices=Designation.choices, blank=True)
    service_location = models.CharField(max_length=120, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.get_designation_display() or 'N/A'}"


# signal to auto-create a blank profile for new users
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # create a profile automatically when a new User is created
        PractitionerProfile.objects.create(user=instance)
    else:
        # ensure profile exists in case it was missing
        PractitionerProfile.objects.get_or_create(user=instance)
