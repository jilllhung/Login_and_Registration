from django.db import models
from django.utils import timezone
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #check password and email basic format
        if postData["password"] == "":
            errors["password_input"] = "Password is required"
        elif len(postData["password"]) < 8:
            errors["password_length"] = "Password should be at least 8 characters" 
        if postData["email"] == "":
            errors["email_input"] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email_format'] = "Invalid email address!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.TextField(max_length = 500)
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 150)
    birthday = models.DateField(default = timezone.now)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return f"<User object: {self.first_name} {self.last_name} ({self.id})>"