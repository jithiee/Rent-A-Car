from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  

    path('cars_list/',views.cars,name='cars'),
    path('booking/<int:car_id>/', views.booking, name='booking'),
    path('payment/<int:book_id>/', views.payment, name='payment'),
    path('success/', views.success, name='success')

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

