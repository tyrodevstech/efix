from core.utils import get_months
from .forms import *
def invoiceform(request):
    form = InvoiceForm()
    context = {
        'invoiceform':form,
    }
    return context


def get_mdod(request):
    month_fday,month_lday = get_months()
    monthlyDue=0
    totalDue=0

    invoiceListforMonth = Invoice.objects.filter(created_at__range=[month_fday,month_lday])
    for i in invoiceListforMonth:
        if i.status == 'Unpaid':
            # monthlyDue += (i.tech_charge + i.equip_charge)
            pass


    invoiceList = Invoice.objects.filter()
    for i in invoiceList:
        if i.status == 'Unpaid':
            # totalDue += (i.tech_charge + i.equip_charge)
            pass


    context={
        'overAllDue': totalDue,
        'monthlyDue': monthlyDue
    }
    return context