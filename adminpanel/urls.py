
from django.urls import path
from . import views 

urlpatterns = [
   
     path('login_admin/',views.login_admin_view, name='login_admin' ),
     path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard' ),
     path('admin_dashboard/user/',views.admin_users_view, name='admin_user' ),
     path('admin_dashboard/cars/',views.admin_cars_view, name='admin_cars' ),
     path('admin_dashboard/car-fleet/', views.admin_create_car, name='car_fleet_management'),
     path('admin_dashboard/book-pay-details/', views.admin_booking_payment_deatils, name='book_payment'),
    
]