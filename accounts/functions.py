import string
import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import loader
from django.conf import settings

def password_generator():
    characters = string.ascii_letters + string.punctuation + string.digits
    pswd_length = random.randint(8, 16)
    for x in range(pswd_length):
        pswd = random.choice(characters)
    return pswd


def new_admin_notification(admin_staff_no, admin_email):
    to_email = settings.ADMINS
    message = "A new admin has been registered"
    subject = "New User Registration Notification."
    try:
        html_content = loader.render_to_string('accounts/admin_email_template.html', {'staff_number': admin_staff_no, 'email':admin_email})
        email_message = EmailMultiAlternatives(subject, message, None, [to_email])
        
        email_message.attach_alternative(html_content, mimetype='text/html')
        email_message.send()
        # return True
    except Exception as e:
        print("Email(new admin notif.) sending failed with", e)
        # return False


def admin_reg_email(admin_pswd, admin_email):
    message = "You have been successfully added as an admin in the emergency dept."
    to_email = admin_email
    subject = "Emergency Dept. Admin Registration Notification."
    try:
        html_content = get_template('accounts/admin_reg_email_template.html').render({'password': admin_pswd, 'email':admin_email})
        email_message = EmailMultiAlternatives(subject, message, None, [to_email])
        email_message.attach_alternative(html_content, mimetype='text/html')
        email_message.send()
        # return True
    except Exception as e:
        print("Email(admin reg) sending failed with", e)
        # return False
   
def staff_reg_email(staff_pswd, staff_email):
    message = "You have been successfully added as staff in the emergency dept."
    to_email = staff_email
    subject = "Emergency Dept. Staff Registration Notification."
    try:
        # html_content = get_template('accounts/staff_reg_email.html').render({'password': staff_pswd, 'email':staff_email})
        html_content = loader.render_to_string('accounts/staff_reg_email.html', {'password': staff_pswd, 'email':staff_email})
        email_message = EmailMultiAlternatives(subject, message, None, [to_email])
        email_message.attach_alternative(html_content, mimetype='text/html')
        email_message.send()
        # return True
    except Exception as e:
        print("Email(admin reg) sending failed with", e)
        # return False

    
def superuser_reg_email(admin_pswd, admin_email):
    message = "You have been successfully added as an admin."
    to_email = admin_email
    subject = "Admin Registration Notification."
    try:
        html_content = loader.render_to_string('accounts/admin_reg_email_template.html', {'password': admin_pswd, 'email':admin_email})
        email_message = EmailMultiAlternatives(subject, message, None, [to_email])
        email_message.attach_alternative(html_content, mimetype='text/html')
        email_message.send()
        # return True
    except Exception as e:
        print("Email(admin reg) sending failed with", e)
        # return False
