from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import InvoiceForm
from .models import Invoice
from django.db.models import Sum
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from rest_framework import viewsets 
from .serializers import InvoiceSerializer
from rest_framework.permissions import IsAuthenticated



class InvoiceViewset(viewsets.ModelViewSet):
    queryset= Invoice.objects.all()
    serializers_class = InvoiceSerializer
    Permission_class= (IsAuthenticated)



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect('home')
    else:
        form = InvoiceForm()

    # Get all invoices for this user
    invoices = Invoice.objects.filter(user=request.user).order_by('-date')

    # Analytics
    total_invoices = invoices.count()
    total_amount = invoices.aggregate(Sum('amount'))['amount__sum'] or 0
    paid_count = invoices.filter(status='paid').count()
    unpaid_count = invoices.filter(status='unpaid').count()

    context = {
        'form': form,
        'invoices': invoices,
        'total_invoices': total_invoices,
        'total_amount': total_amount,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
    }

    return render(request, 'invoice/home.html', context)


from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from django.urls import reverse

def invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    html_string = render_to_string('invoice/invoice_pdf.html', {'invoice': invoice})

    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{invoice.id}.pdf'
    response.write(result)
    return response


from django.shortcuts import get_object_or_404

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoice_detail.html', {'invoice': invoice})


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'invoice': invoice})

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})



def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')
