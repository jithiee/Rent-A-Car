    
from django import forms
from .models import BookingCar
from datetime import date
from django.core.validators import MinValueValidator

class CarBookingForms(forms.ModelForm):
    class Meta:
        model = BookingCar
        fields = ['picking_date', 'return_date', 'total_days']
        widgets = {
            'picking_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }
        today = date.today()
        picking_date = forms.DateField(validators=[MinValueValidator(today)])

        def clean(self):
            cleaned_data = super().clean()
            picking_date = cleaned_data.get('picking_date')
            return_date = cleaned_data.get('return_date')

            if picking_date and return_date:
                if return_date < picking_date:
                    raise forms.ValidationError("Return date must be greater than or equal to picking date.")