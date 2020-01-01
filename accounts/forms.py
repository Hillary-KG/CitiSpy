import random
from django.utils.translation import ugettext as _
from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email, RegexValidator 
from .functions import admin_reg_email, new_admin_notification
from django.contrib.auth.hashers import make_password

class  LoginForm(forms.Form):
    """LoginForm: User auth form"""
    #form fields 
    email = forms.EmailField(max_length=50,label="Email Address", widget=forms.EmailInput(attrs={'name':"email", 'placeholder': "Email Address", 'class':"form-control input-sm bounceIn animation-delay2"})
                            ,validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password", 
                'class':"form-control specialinput first",'name':"password",  'autocomplete':"off"}))
    class Meta:
        fields = ['email', 'password']

class RegisterAdmin(forms.ModelForm):
    TYPES = (
        ('SU', 'Super User'),
        ('DEPT. ADMIN', 'Dept. Admin'),
        ('DEPT. STAFF', 'Dept. Staff')
    )
    first_name = forms.CharField(max_length=30,label="Fist Name", widget=forms.TextInput(attrs={'name':"first_name", 'class':"form-control input-sm bounceIn animation-delay2"}))
    last_name = forms.CharField(max_length=30,label="Last Name", widget=forms.TextInput(attrs={'name':"last_name", 'class':"form-control input-sm bounceIn animation-delay2"}))
    # username = forms.CharField(max_length=30,label="Username", widget=forms.TextInput(attrs={'name':"username",'class':"form-control input-sm bounceIn animation-delay2"}))
    staff_number = forms.CharField(max_length=10,label="Staff Number", widget=forms.TextInput(attrs={'name':"staff_number", 'class':"form-control input-sm bounceIn animation-delay2"}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',label="Phone Number", error_messages={'required':"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."},
                            widget=forms.TextInput(attrs={'name':"phone_number", 'class':"form-control input-sm bounceIn animation-delay2"}))
    email = forms.EmailField(max_length=255,label="Email Address", widget=forms.EmailInput(attrs={'name':"email", 'class':"form-control input-sm bounceIn animation-delay2"}), 
                    validators=[validate_email])
    admin_type = forms.ChoiceField(required=True, choices=TYPES, widget=forms.RadioSelect(attrs={'name':"admin_type", 'class':"form-control input-sm bounceIn animation-delay2"}))
    # profile_pic = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'name':"profile_pic", 'class':"form-control input-sm bounceIn animation-delay2",
                            # }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']
    
    # def clean_admin_type(self):
    #     # print(self.cleaned_data)
    #     email = self.cleaned_data['email']
    #     if self.cleaned_data['admin_type'] == 'SU' and User.objects.filter(email=email, is_superuser=True).exists():
    #         raise forms.ValidationError(_("A superuser with the entered email address already exists"), code="su exists")
    #     if self.cleaned_data['admin_type'] == 'DEPT. STAFF' and User.objects.filter(email=email, account_type=2).exists():
    #         raise forms.ValidationError(_("A Staff with the entered email address already exists"), code="staff exists")
    #     if self.cleaned_data['admin_type'] == 'DEPT. ADMIN' and User.objects.filter(email=email, account_type=1).exists():
    #         raise forms.ValidationError(_("An admin with the entered email address already exists"), code="admin exists")

    def save(self, commit = True, *args, **kwargs):
        admin = super(RegisterAdmin, self).save(commit=False, *args, **kwargs)
        print("admin here",self.cleaned_data)
        if commit:
            email = self.cleaned_data['email']
            if self.cleaned_data['admin_type'] == 'SU' and User.objects.filter(email=email, is_superuser=True).exists():
                raise forms.ValidationError(_("A superuser with the entered email address already exists"), code="su exists")
            if self.cleaned_data['admin_type'] == 'DEPT. STAFF' and User.objects.filter(email=email, account_type=2).exists():
                raise forms.ValidationError(_("A Staff with the entered email address already exists"), code="staff exists")
            if self.cleaned_data['admin_type'] == 'DEPT. ADMIN' and User.objects.filter(email=email, account_type=1).exists():
                raise forms.ValidationError(_("An admin with the entered email address already exists"), code="admin exists")
            if self.cleaned_data['admin_type'] == 'SU':
                admin.is_superuser = True
                admin.account_type = 1
                admin.is_staff = True
            if self.cleaned_data['admin_type'] == 'DEPT. ADMIN':
                admin.account_type = 2
                admin.is_staff = True
            if self.cleaned_data['admin_type'] == 'DEPT. STAFF':
                admin.account_type = 3
                admin.is_staff = True
            plain_pswd = 'admin' + str(random.randint(999, 9999))
            admin.password = make_password(plain_pswd)
            print("plain", plain_pswd)
            
            if new_admin_notification(admin.staff_number, admin.email) and admin_reg_email(plain_pswd, admin.email):
                admin.save()
            
            

        


class RegisterUserForm(forms.ModelForm):
    error_css_class = "error"
    required_css_class = "required"
    username = forms.CharField(max_length=25,label="Username", widget=forms.TextInput(attrs={'name':"username",'class':"form-control input-sm bounceIn animation-delay2", 'placeholder': "Username"}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',label="Phone Number", error_messages={'required':"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."},
                            widget=forms.TextInput(attrs={'name':"phone_number", 'class':"form-control input-sm bounceIn animation-delay2", 'placeholder': "Phone Number"}))
    email = forms.EmailField(max_length=255,label="Email Address", widget=forms.EmailInput(attrs={'name':"email", 'placeholder': "Email Address", 'class':"form-control input-sm bounceIn animation-delay2"})
                            ,validators=[validate_email])
    password = forms.CharField(max_length=250, label='Password',widget=forms.PasswordInput(attrs={'placeholder':"Password", 
                'class':"form-control specialinput first",'name':"password",  'autocomplete':"off"}))
    confirm_password = forms.CharField(max_length=250, label='Password',widget=forms.PasswordInput(attrs={'placeholder':"Password", 
                'class':"form-control specialinput first",'name':"confirm_password",  'autocomplete':"off"}))

   
    class Meta:
        model = User
        fields = ['username', 'email','phone_number', 'password', 'confirm_password']

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        password_confirm = self.cleaned_data["confirm_password"]
        if password != password_confirm:
            raise forms.ValidationError(_("Your passwords do not match"), code="password mismatch")
            return password_confirm
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email, account_type=3).exists:
            raise forms.ValidationError(_("A user with the entered email address already exists"), code="user exists")



class ChangePasswordForm():
    old_password = forms.CharField(max_length=250, label='Old Password',widget=forms.PasswordInput(attrs={'placeholder':"Old Password", 
                'class':"form-control specialinput first",'name':"old_password",  'autocomplete':"off"}))
    new_password = forms.CharField(max_length=250, label='New Password',widget=forms.PasswordInput(attrs={'placeholder':"New Password", 
                'class':"form-control specialinput first",'name':"new_password",  'autocomplete':"off"}))
    confirm_new_password = forms.CharField(max_length=250, label='Confirm New Password',widget=forms.PasswordInput(attrs={'placeholder':"COnfirm New Password", 
                'class':"form-control specialinput first",'name':"confirm_new_password",  'autocomplete':"off"}))
    
    class Meta:
        fields = ['old_password', 'new_password', 'confirm_new_password']
    
    def clean_old_password(self):
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError(_("Wrong Old Password"), code='wrong password')

    def clean_confirm_new_password(self):
        if self.cleaned_data['confirm_new_password'] != self.cleaned_data['new_password']:
            raise ValidationError(_("New passowrds did not match. Please try again."), code="password mismatch")
    








    
    