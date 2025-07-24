
from django import forms
from .models import Invoice

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client_name', 'client_email', 'description', 'amount', 'status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('client_name', css_class='w-full'),
                Column('client_email', css_class='w-full'),
            ),
            'description',
            'amount',
            'status',
            Submit('submit', 'Generate Invoice', css_class='bg-red-600 text-white px-4 py-2 rounded')
        )
