from django.shortcuts import render ,get_object_or_404 , redirect
from .models import Vehicle
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import date 
from .models import BookingCar
from datetime import datetime
from django.contrib import messages
from .forms import CarBookingForms
from .models import BookingCar,PaymentDetails
from django.conf import settings
import uuid
import razorpay
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from xhtml2pdf import pisa
from io import BytesIO




def cars(request):
    Vehicles = Vehicle.objects.filter(is_available=True)
    today = date.today()    

    # Dictionary: car_id -> return_date in ISO format
    booked_car_info = {}

    for car in Vehicles:
        latest_booking = BookingCar.objects.filter(car=car ,is_paid=True ).order_by('-return_date').first()
        if latest_booking and latest_booking.return_date >= today:
            booked_car_info[car.id] = latest_booking.return_date.strftime('%Y-%m-%dT00:00:00')

    context = {
        'Vehicles': Vehicles,
        'booked_cars': booked_car_info,  # dict: car_id -> return date string
    }
    return render (request , 'cars/cars_list.html' , context)





def booking(request, car_id=None):
    vehicle = get_object_or_404(Vehicle, id=car_id)

    if request.method == 'POST':
        form = CarBookingForms(request.POST)  

        pdate_str = request.POST.get('picking_date')
        rdate_str = request.POST.get('return_date')
        
        date_format = "%Y-%m-%d"  # Adjust this to match your input format
        picking_date = datetime.strptime(pdate_str, date_format).date()
        return_date = datetime.strptime(rdate_str, date_format).date()
        
        total_days = (return_date - picking_date).days
      
        
        if not pdate_str or not rdate_str:
            messages.error(request, "Both picking and return dates are required.")
        else:
            try:
                pdate = datetime.strptime(pdate_str, '%Y-%m-%d')
                rdate = datetime.strptime(rdate_str, '%Y-%m-%d')
                
                if pdate.date() < datetime.today().date():
                    messages.error(request, 'Picking date must be in the future.')
                elif pdate > rdate:
                    messages.error(request, 'Return date must be after picking date.')
                elif form.is_valid():
                    booking = form.save(commit=False)
                    booking.car = vehicle
                    booking.total_days = total_days
                    booking.unique_id = uuid.uuid4().hex[:12]
                    
                    if request.user.is_authenticated:
                        booking.user = request.user
                    booking.save()
                    
                    return redirect('payment', book_id=booking.id)
                    
                else:
                    messages.error(request, 'Form is not valid.')
            except ValueError:
                messages.error(request, 'Invalid date format.')

    else:
        form = CarBookingForms()  

    return render(request, 'cars/booking.html', {
        'car': vehicle,
        'form': form,
    })


def payment(request, book_id):
    forms = CarBookingForms()
    book = get_object_or_404(BookingCar, id=book_id)

    picking_date = book.picking_date
    return_date = book.return_date
    total_days = (return_date - picking_date).days
    # amount = book.car.price * total_days * 100  # Razorpay needs amount in paise
    amount_in_paise = book.car.price * book.total_days * 100

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

    
    # Create Razorpay Order
    payment = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Optional: Save order_id to DB
    book.razorpay_order_id = payment['id']
    book.save()

    context = {
        'booking_id': book_id,
        'book': book,
        'amount': amount_in_paise // 100,  # Show in INR
        'total_days': total_days,
        'unique_id': book.unique_id,
        'razorpay_key': settings.RAZORPAY_KEY_ID,  
        'form': forms,
        'payment': payment  # pass this to template!
    }
    return render(request, 'cars/payment.html', context)

def success(request):
    payment_id = request.GET.get("razorpay_payment_id")
    book_id    = request.GET.get("booking_id")
    booking    = get_object_or_404(BookingCar, id=book_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,
                                   settings.RAZORPAY_SECRET_KEY))

    try:
        payment = client.payment.fetch(payment_id)
        PaymentDetails.objects.create(
            razor_payment_id = payment_id,
            user            = booking.user,
            booking         = booking,
            amount_paid     = payment["amount"] / 100,
            razor_pay_status= payment["status"],
        )
        booking.is_paid = True
        booking.save()
        # send_invoice_pdf(booking, payment["amount"] / 100)
        
    except razorpay.errors.BadRequestError as e:
        return HttpResponse(f"Razorpay error : {e}")

    return render(request, 'cars/success.html', {"book": booking})


# def send_invoice_pdf(booking, amount):
#     html = render_to_string('cars/invoice.html', {'booking': booking, 'amount': amount})
#     result = BytesIO()
#     pisa_status = pisa.CreatePDF(html, dest=result)

#     if pisa_status.err:
#         return None

#     pdf = result.getvalue()
#     email = EmailMessage(
#         'Your Booking Invoice - DriveEase Rentals',
#         'Please find your booking invoice attached.',
#         settings.DEFAULT_FROM_EMAIL,
#         [booking.user.email],
#     )
#     email.attach(f'Invoice_{booking.unique_id}.pdf', pdf, 'application/pdf')
#     email.send()
    
    