from django.contrib import admin
from .models import Payments, Order, OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display  = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_orderd', 'created_at']
    list_filter   = ['state', 'is_orderd']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20

admin.site.register(Payments)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)