from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('Dashboard/', views.home, name='home'),
    path('invoice/<int:invoice_id>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:pk>/delete/', views.delete_invoice, name='delete_invoice'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),



]
# This file defines the URL patterns for the invoice app.