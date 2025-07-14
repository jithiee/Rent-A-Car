from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin ):
    list_display = ('email','first_name','last_name','phone_number','date_joined','username','last_login','is_active',)
    list_display_links =('email','first_name','last_name',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    
    search_fields =['phone_number',] # admin seach filed
    
    filter_horizontal = () #for making password read only
    list_filter = ()     #for making password read only
    fieldsets = ()  #for making password read only
admin.site.register(Account,AccountAdmin)    