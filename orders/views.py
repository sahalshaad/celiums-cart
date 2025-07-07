import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
import razorpay

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order


from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payments, OrderProduct
# Create your views here.

def payments(request):
    return render (request, 'orders/payments.html')



def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    # if the cart count is less than or equel to zero, then redirect to shop
    cart_item = CartItem.objects.filter(user=current_user)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect ('store')
    
    grand_total = 0
    tax         = 0
    for cart_items in cart_item:
        total += (cart_items.product.price * cart_items.quantity)
        quantity += cart_items.quantity #77 6:23
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside the table
            data = Order()
            data.user = current_user 
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line1  = form.cleaned_data['address_line1']
            data.address_line2  = form.cleaned_data['address_line2']
            data.city           = form.cleaned_data['city']
            data.country        = form.cleaned_data['country']
            data.state          = form.cleaned_data['state']
            data.order_notes    = form.cleaned_data['order_notes']
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            # Step 3: Create Razorpay Order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                'amount': int(grand_total * 100),  # amount in paise
                'currency': 'INR',
                'payment_capture': '1'
            })

            # Step 4: Store razorpay_order_id in DB
            data.razorpay_order_id = razorpay_order['id']
            data.save()
            

            context = {

                'order': data,
                'cart_items': cart_item,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': int(grand_total * 100),
            }
            return render (request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
        
# ChatGPT
@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        # Step 1: Extract Razorpay data
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        order_number = request.POST.get('order_id')

        # Step 2: Get the order
        order = Order.objects.get(order_number=order_number, is_orderd=False)
        order.payment_method = "Razorpay"  # optional
        order.is_orderd = True
        order.save()

        # Step 3: Create Payment entry
        payment = Payments(
            user=request.user,
            payment_id=razorpay_payment_id,
            payment_method="Razorpay",
            amount_paid=order.order_total,
            status="Success"
        )
        payment.save()

        # Step 4: Link Payment to Order
        order.payment = payment
        order.save()

        # Step 5: Move Cart Items to OrderProduct
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment
            order_product.user = request.user
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.color = item.variations.first().variation_value if item.variations.exists() else ""
            order_product.size = item.variations.last().variation_value if item.variations.exists() else ""
            order_product.variation = item.variations.first() if item.variations.exists() else None
            order_product.ordered = True
            order_product.save()

            # Optional: Update stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Step 6: Clear cart
        cart_items.delete()

        # Step 7: Show success page
        return render(request, 'orders/payment_success.html', {'order': order, 'payment': payment})

    else:
        return redirect('store')

