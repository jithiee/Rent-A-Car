from django.db import models
from accounts.models import Account
from django.utils import timezone


class Vehicle(models.Model):
    def __str__(self):
        return f"{self.year} {self.make} - {self.transmission}"
    
    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
      
    ]
    
    FUEL_TYPE = [
        ('Diesel','Diesel'),
        ('Petrol','Petrol'),
        ('Electric','Electric')
    ]
    
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField() 
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    car_img = models.ImageField(upload_to='vehicle_images/')  
    price = models.IntegerField(default=0) 
    is_available = models.BooleanField(default=True)    
    description = models.TextField(max_length=500, blank=True)
    color = models.CharField(max_length=25)
    fuel = models.CharField(max_length=25,choices=FUEL_TYPE)
    is_status = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)


    def __str__(self):
        return f"  {self.make}   {self.transmission} {self.year} "
    
    
    

class BookingCar(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    car = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    picking_date = models.DateField()
    return_date = models.DateField()
    total_days= models.IntegerField(default=0 , null=True , blank=True)
    is_paid = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    def __str__(self):
        return f"{self.user}"

    

class PaymentDetails(models.Model):
    razor_payment_id = models.CharField(max_length=255)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    booking = models.ForeignKey(BookingCar,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=100) # this is the total amount
    razor_pay_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.razor_payment_id)

    

    
    
    
 