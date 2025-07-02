from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.
def place_order(request):
    current_user = request.user
    
    # if the cart count is less than or equel to zero, then redirect to shop
    cart_item = CartItem.objects.filter(user=current_user)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect ('store')
    
    grand_total = 0
    tax         = 0
    for cart_items in cart_item:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity #77 6:23
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside the table
            data = Order()
            data.first_name     = form.cleaned_data('first_name')
            data.lirst_name     = form.cleaned_data('lirst_name')
            data.phone          = form.cleaned_data('phone')
            data.email          = form.cleaned_data('email')
            data.address_line1  = form.cleaned_data('address_line1')
            data.address_line2  = form.cleaned_data('address_line2')
            data.city           = form.cleaned_data('city')
            data.country        = form.cleaned_data('country')
            data.state          = form.cleaned_data('state')
            data.order_notes    = form.cleaned_data('order_notes')
            data.order_total    = form.cleaned_data('order_total')
            