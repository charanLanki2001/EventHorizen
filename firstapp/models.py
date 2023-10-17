from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    college_website = models.CharField(max_length=200)
    event_datetime = models.DateTimeField(blank=True, null=True)
    event_description = models.TextField()
    event_brochure = models.FileField(upload_to='event_brochures/', blank=True, null=True)
    coordinator_name = models.CharField(max_length=100)
    coordinator_contact = models.CharField(max_length=20)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.event_name  
    
   
class Payment(models.Model):
    email = models.EmailField()
    payment_date = models.DateTimeField(auto_now_add=True)
    eventname = models.CharField(max_length=100)  # Added event_name field
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added amount field
    
    def __str__(self):
        return self.email