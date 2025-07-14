from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts . models import Account
from cars . models import BookingCar ,PaymentDetails
from django.core.paginator import Paginator
from django.db.models import Q , Count
from cars . models import Vehicle
from django.utils import timezone
from django.db.models import Prefetch




def login_admin_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.role == 'superadmin' and user.is_active and user.is_superadmin:
                auth.login(request, user)
                return redirect('admin_dashboard')  # change this to your admin home page
            else:
                messages.error(request, 'Access denied. Not an admin account.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'admin/auth/login_admin.html')

def admin_dashboard(request):
    return render(request , 'admin/admin_dashboard/dashboard.html')



def admin_users_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    users = Account.objects.all()

    # Search by name or email
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Filter by status
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    # Prepare data with booking counts
    user_data = []
    for user in users:
        bookings_count = BookingCar.objects.filter(user=user).count()
        user_data.append({
            'user': user,
            'bookings': bookings_count
        })

    # Paginate results (10 per page)
    paginator = Paginator(user_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_data': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'page_obj': page_obj,
    }
    return render(request, 'admin/admin_dashboard/users.html', context)

def admin_cars_view(request):
    today = timezone.now().date()

    vehicles = Vehicle.objects.all()
    
    # Cars currently booked
    currently_rented_ids = BookingCar.objects.filter(
        picking_date__lte=today,
        return_date__gte=today
    ).values_list('car_id', flat=True)

    total_cars = vehicles.count()
    available_cars = vehicles.exclude(id__in=currently_rented_ids).count()
    rented_cars = vehicles.filter(id__in=currently_rented_ids).count()
    booked_cars = Vehicle.objects.filter(bookingcar__isnull=False).distinct()
    maintenance_cars = vehicles.filter(is_status=True).count()  # If is_status means under maintenance

    context = {
        'vehicles': vehicles,
        'total_cars': total_cars,
        'available_cars': available_cars,
        'rented_cars': rented_cars,
        'booked_cars': booked_cars,
        'maintenance_cars': maintenance_cars,
        'rented_ids': list(currently_rented_ids),  # Pass to template
    }
    return render(request, 'admin/admin_dashboard/car_admin.html', context)



def admin_create_car(request):
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = request.POST.get('year')
        transmission = request.POST.get('transmission')
        car_img = request.FILES.get('car_img')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'on'
        description = request.POST.get('description')
        color = request.POST.get('color')
        fuel = request.POST.get('fuel')

        Vehicle.objects.create(
            make=make,
            model=model,
            year=year,
            transmission=transmission,
            car_img=car_img,
            price=price,
            is_available=is_available,
            description=description,
            color=color,
            fuel=fuel
        )
        messages.success(request, "New vehicle added successfully.")
        return redirect('car_fleet_management')
    
    # For GET requests
    vehicles = Vehicle.objects.all()
    total_cars = vehicles.count()
    available_cars = vehicles.filter(is_available=True).count()
    rented_cars = vehicles.filter(is_available=False).count()
    maintenance_cars = 0  # Adjust logic if you track maintenance status

    context = {
        'vehicles': vehicles,
        'total_cars': total_cars,
        'available_cars': available_cars,
        'rented_cars': rented_cars,
        'maintenance_cars': maintenance_cars,
    }
    return render(request, 'admin/admin_dashboard/car_admin.html', context)



def admin_booking_payment_deatils(request):
    today = timezone.now().date()

    # Prefetch payment details for each booking
    payment_qs = PaymentDetails.objects.select_related('user')
    bookings_qs = BookingCar.objects.select_related('user', 'car').prefetch_related(
        Prefetch('paymentdetails_set', queryset=payment_qs)
    ).order_by('-created_at')

    total_bookings = bookings_qs.count()
    active_bookings = bookings_qs.filter(picking_date__lte=today, return_date__gte=today).count()
    completed_bookings = bookings_qs.filter(return_date__lt=today).count()
    cancelled_bookings = 0

    paginator = Paginator(bookings_qs, 10)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
    }
    return render(request, 'admin/admin_dashboard/booking_payment.html', context)
 



