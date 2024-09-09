from django.contrib import admin
from .models import Order, OrderItem
import openpyxl
from django.http import HttpResponse


# Register your models here.
def export_to_exel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=order.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Orders'
    columns = ['ID', 'First name', 'Last name', 'phone', 'address', 'Paid', 'created']
    ws.append(columns)
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([order.id,
                   order.first_name,
                   order.last_name,
                   order.phone,
                   order.address,
                   order.paid,
                   created, ])
    wb.save(response)
    return response


export_to_exel.short_description = 'Export_to_Exel'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'first_name', 'first_name', 'last_name', 'phone', 'address', 'postal_code',
                    'province', 'city',
                    'created', 'updated', 'paid']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
    actions = [export_to_exel]
