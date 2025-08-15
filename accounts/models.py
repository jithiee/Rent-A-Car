from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.core.validators import RegexValidator

#creating for super admin
class MyAccountManager(BaseUserManager):
    
    def create_user(self,first_name ,last_name ,username, email ,password=None  ):
        if not email :
             raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username') 
      
        user = self.model(
            email = self.normalize_email(email) ,   #enter any capital letter email the  normalize_email make to smalletter
            username = username,
            first_name = first_name,
            last_name = last_name,  
        )
        
        user.set_password(password) 
        user.save(using=self._db) # 
        return user
    
    # creating superuser
    def create_superuser(self,first_name ,last_name ,username, email ,password):
          user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password,
            first_name = first_name,
            last_name = last_name
        )
          # superuser permitions
          user.is_admin = True
          user.is_staff = True
          user.is_active =True
          user.is_superadmin = True

          user.save(using=self._db ) # _db save the database or db connection
          return user
          
   
   #account model  
   
   
   
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    
    # New profile fields
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    profile_picture = models.ImageField(upload_to='user_profile/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('superadmin', 'Super Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):  # a person is_admin he can all permitons to change everything 
        return self.is_admin
    
    def has_module_perms(self,add_label):     # Check if the user has the appropriate permissions for the module
        return True
    
    
