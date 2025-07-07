from django.db import models

from accounts.models import Account
from store.models import Product, Variation

# Create your models here.

class Payments(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=100)
    payment_method  = models.CharField(max_length=100)
    amount_paid     = models.CharField(max_length=100) # total amount field
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS          = (
        ('Now', 'Now'),
        ('Accepted', 'Accepted'),
        ('Compleated', 'Compleated'),
        ('Cancelled', 'Cancelled'),
        
    )
    
    user           = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment        = models.ForeignKey(Payments, on_delete=models.SET_NULL, blank=True, null=True)
    order_number   = models.CharField(max_length=100)
    first_name     = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    phone          = models.CharField(max_length=15)
    email          = models.EmailField(max_length=50)
    address_line1  = models.CharField(max_length=100)
    address_line2  = models.CharField(max_length=100, blank=True)
    city           = models.CharField(max_length=100)
    country        = models.CharField(max_length=100)
    state          = models.CharField(max_length=100)
    order_total    = models.FloatField(max_length=100)
    order_notes    = models.CharField(max_length=100)
    tax            = models.FloatField()
    status         = models.CharField(max_length=10, choices=STATUS, default="Now")
    ip             = models.CharField(blank=True, max_length=20)
    is_orderd      = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)

    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
        
    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payments, on_delete=models.CASCADE)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation       = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color           = models.CharField(max_length=50)
    size            = models.CharField(max_length=50)    
    quantity        = models.IntegerField()    
    product_price   = models.FloatField()    
    ordered         = models.BooleanField(default=False)    
    cfreated_at     = models.DateTimeField(auto_now_add=True)    
    updated_at      = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return self.product.product_name
      

    