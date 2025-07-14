from django.shortcuts import render,redirect
from . forms import RegistrationForm
from . models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.contrib.auth import logout as django_logout 
from .forms import UserProfileForm, CustomPasswordChangeForm
from cars.models import BookingCar
from datetime import date
from django.utils import timezone



 
def home(request):
    return render(request , 'home/home.html')

def about(request):
    return render(request , 'home/about.html')
def contact(request):
    return render(request , 'home/contact.html')

 
 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.is_active = False
            user.save()

            # Send email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('registration/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_obj = EmailMessage(mail_subject, message, to=[email])
            email_obj.send()

            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


  
  # email activation 
def activate(request,uidb64,token):
   try :
       uid = urlsafe_base64_decode(uidb64).decode()
       print(uid)
       user =  Account.objects.get (pk = uid)
   except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
       user = None
   if user is not None and default_token_generator.check_token(user,token):
       user.is_active = True
       user.save()
       messages.success(request,'congratulaions your account  is activated') 
       return redirect('login')
   else:
       messages.error(request,'Invalid activation link') 
       return redirect('register')
    


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
       

        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')

    return render(request, 'registration/login.html')



def logout(request):
    django_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('register')


def foregotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email = email)# iexact caseseciteve
            
            #Reset password email
            current_site = get_current_site(request)
            mail_subject = "reset your password"  # Fixed type here
            print('2')
            message = render_to_string('resetpassword_email.html',{
               'user':user,
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)), #user id
               'token':default_token_generator.make_token(user),
            })
            print('3')

            to_email = email
            sent_email = EmailMessage(mail_subject, message, to=[to_email])
            sent_email.send() 
            
            messages.success(request,'passwod reset email has email your email address') 
            return redirect('login')

        else :
            messages.error(request,'Account doese not exist !') 
            return redirect ('foregotpassword')   
    
        
        
    return render (request, 'foregotpassword.html' )


        
@login_required(login_url = 'login')  
def user_profile(request):
    user = request.user
    total_bookings = BookingCar.objects.filter(user=user).count()
    active_bookings = BookingCar.objects.filter(user=user, return_date__gte=date.today()).count()
    loyalty_points = user.loyalty_points if hasattr(user, 'loyalty_points') else 0   # Now i dont get this logic i will create this in the future
    current_bookings = BookingCar.objects.filter(user=user, return_date__gte=date.today()).order_by('-picking_date')
   
    recent_activity = BookingCar.objects.filter(user=user).order_by('-picking_date')[:5]
    
    context = {
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'loyalty_points': loyalty_points,
        'current_bookings': current_bookings,
        'recent_activity': recent_activity,
        'today': date.today()
    }
 
    
    return render (request ,'user_profile/profile.html'  , context)
      


@login_required(login_url='login')
def user_profile_update(request):
    user = request.user
    
    if request.method == 'POST':
        # Handle profile update
        if 'saveProfileBtn' in request.POST:
            user.first_name = request.POST.get('firstName', '')
            user.last_name = request.POST.get('lastName', '')
            user.phone_number = request.POST.get('phone', '')
            user.address = request.POST.get('address', '')
            user.city = request.POST.get('city', '')
            user.country = request.POST.get('country', '')
            
            # Handle profile picture upload
            if 'fileUpload' in request.FILES:
                user.profile_picture = request.FILES['fileUpload']
            
            user.save()
            messages.success(request, 'Profile updated successfully!')
            # return redirect('userprofile') // javascript hanhile with some desly and reditect 
        
        # Handle password change
        elif 'changePasswordBtn' in request.POST:
            current_password = request.POST.get('currentPassword', '')
            new_password = request.POST.get('newPassword', '')
            confirm_password = request.POST.get('confirmPassword', '')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect!')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match!')
            else:
                user.set_password(new_password)
                user.save()
                auth.update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Password changed successfully!')
            
            return redirect('user_profile_update')
    
    # Get countries list for the dropdown
    countries = ['United States', 'Canada', 'Mexico', 'United Kingdom']
    
    context = {
        'user': user,
        'countries': countries,
    }
    return render(request, 'user_profile/profile_update.html', context)







