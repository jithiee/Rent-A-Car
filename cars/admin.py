from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin 



class BokkAdmin(admin.ModelAdmin):
    list_display=['id','user','car','picking_date','return_date' , 'total_days', 'unique_id']
    list_display_links=['id','user']
admin.site.register(BookingCar,BokkAdmin)

class PayAdmin(admin.ModelAdmin):
    list_display = ['razor_payment_id','user',]

admin.site.register(PaymentDetails,PayAdmin)

from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'transmission', 'fuel', 'price', 'is_available'  , 'is_status']
    list_filter = ['transmission', 'fuel', 'is_available', 'year']
    search_fields = ['make', 'model', 'color']


