from django.urls import path, include
from rest_framework.routers import DefaultRouter
from invoice.views import InvoiceViewset

router = DefaultRouter()
router.register(r'invoices', InvoiceViewset)

urlpatterns = [
    path('api/', include(router.urls)),
]
