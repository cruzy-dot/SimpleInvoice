from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# This file defines the models for the invoice app.

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.client_name} - ${self.amount}"
    

    
    