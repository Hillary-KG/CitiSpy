from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email, RegexValidator 

class  LoginForm(forms.Form):
    """docstring for  LoginForm"""
    #form fields 
    email = forms.EmailField(max_length=50,label="Email Address", widget=forms.EmailInput(attrs={'name':"email", 'placeholder': "Email Address", 'class':"form-control input-sm bounceIn animation-delay2"})
                            ,validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password", 
                'class':"form-control specialinput first",'name':"password",  'autocomplete':"off"}))
    class Meta:
        fields = ['email', 'password']

class RegisterDeptStaff(forms.ModelForm):
    first_name = forms.CharField(max_length=30,label="Fist Name", widget=forms.TextInput(attrs={'name':"first_name", 'class':"form-control input-sm bounceIn animation-delay2"}))
    last_name = forms.CharField(max_length=30,label="Last Name", widget=forms.TextInput(attrs={'name':"last_name", 'class':"form-control input-sm bounceIn animation-delay2"}))
    # user_name = forms.CharField(max_length=30,label="Username", widget=forms.TextInput(attrs={'name':"username",'class':"form-control input-sm bounceIn animation-delay2"}))
    staff_number = forms.CharField(max_length=10,label="Staff Number", widget=forms.TextInput(attrs={'name':"job_number", 'class':"form-control input-sm bounceIn animation-delay2"}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',label="Phone Number", error_messages={'required':"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."},
                            widget=forms.TextInput(attrs={'name':"phone_number", 'class':"form-control input-sm bounceIn animation-delay2"}))
    email = forms.EmailField(max_length=255,label="Email Address", widget=forms.EmailInput(attrs={'name':"email", 'class':"form-control input-sm bounceIn animation-delay2"}), 
                    validators=[validate_email])
    # profile_pic = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'name':"profile_pic", 'class':"form-control input-sm bounceIn animation-delay2",
                            # }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'staff_number']

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



    
    