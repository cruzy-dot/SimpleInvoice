from django.contrib import admin
from .models import Invoice  

admin.site.site_header = "SimpleInvoice Admin"
admin.site.site_title = "SimpleInvoice Admin Portal"
admin.site.register(Invoice)  
# Register your models here.
