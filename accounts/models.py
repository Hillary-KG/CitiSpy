from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractBaseUser):
    '''model that represents a user in the system '''
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
    phone_number = models.CharField(max_length=16,validators=[phone_regex], null=False, blank=False)
    account_type = models.SmallIntegerField(null=False)# 0-superuser, 1-dept admin,2-dept staff, 3-user
    staff_number = models.CharField(max_length=10, blank=False, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # admin_type = models.CharField(max_length=10, blank=False, null=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password'] #fields to be prompted for in creatsuperuser

    def __str__(self):
        return self.first_name+" "+self.last_name
    class META:
        app_label = 'accounts'