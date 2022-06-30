from django import template

register = template.Library()

@register.filter
def add2var(var1,var2):
    return var1+var2



@register.filter
def uppercon(value):
    if value == 'new':
        return 'New'
    elif value == 'in_progress':
        return 'In Progress'
    elif value == 'waittingoncustomer':
        return 'Waitting on Customer'
    elif value == 'fixed':
        return 'Fixed'
    elif value == 'closed':
        return 'Closed'
    elif value == 'cancelled':
        return 'Cancelled'
    else:
        return value