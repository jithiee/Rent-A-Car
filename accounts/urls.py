
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('userprofile/',views.user_profile,name='userprofile'),
    path('profile_update/', views.user_profile_update, name='user_profile_update'),
    
    path('activate/<uidb64>/<token>/',views.activate,name ='activate' ),
  
      
    path('foregotpassword/',views.foregotpassword,name='foregotpassword'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)