# from core.utils import get_months
from .forms import *
def invoiceform(request):
    form = InvoiceForm()
    context = {
        'invoiceform':form,
    }
    return context


def get_mdod(request):
    # month_fday,month_lday = get_months()
    totalPaid=0
    totalDue=0

    # invoiceListforMonth = Invoice.objects.filter(created_at__range=[month_fday,month_lday])
    invoiceList = Invoice.objects.filter()
    for i in invoiceList:
        if i.status == 'Paid':
            totalPaid += (i.tech_charge + i.equip_charge)

    for i in invoiceList:
        if i.status == 'Unpaid':
            totalDue += (i.tech_charge + i.equip_charge)

    context={
        'totalDue': totalDue,
        'totalPaid': totalPaid
    }
    return context