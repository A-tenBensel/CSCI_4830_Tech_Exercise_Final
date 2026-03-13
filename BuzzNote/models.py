from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
  name = models.CharField(max_length = 255)
  phone = PhoneNumberField()
  email = models.EmailField(blank=True) 
  address = models.TextField(blank=True)

  def __str__(self):
    return self.name
  
  