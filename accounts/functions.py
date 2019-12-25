import string
import random

def password_generator():
    characters = string.ascii_letters + string.punctuation + string.digits
    pswd_length = random.randint(8, 16)
    for x in range(pswd_length):
        pswd = random.choice(characters)
    return pswd


# def send_email(recipient):
    

