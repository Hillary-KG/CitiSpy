from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    '''model that represents a user in the system '''
    email = models.EmailField(max_length=255, null=False)
    staff_number = models.CharField(max_length=10, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
    phone_number = models.CharField(max_length=16,validators=[phone_regex], null=False, blank=False)
    account_type = models.IntegerField(null=False)# 1-police, 2-health,3-private emergency response, 4-dept admin, 5-overall-admin
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name+" "+self.last_name
