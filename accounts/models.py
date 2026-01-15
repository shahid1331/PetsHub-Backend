from django.db import models
from django.contrib.auth.models import  AbstractUser,BaseUserManager

class customUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields ):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=extra_fields.get('first_name'),last_name=extra_fields.get('last_name'),phone=extra_fields.get('phone'),)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
class RegisterUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, blank =True,null=False)
    last_name = models.CharField(max_length=100,blank=True,null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = customUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    