from django.db import models
from django.contrib.auth.models import AbstractUser

# user Model
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profiles/' , blank= True, null=True)

    def __str__(self):
        return   str(self.first_name) + ' ' + str(self.last_name)
    
    
# employee
class Employee(models.Model):
    admin = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=50)
    def __str__ (self):
        return str(self.admin)
    
# Payment type
class Payment_type(models.Model):
    title = models.CharField(max_length=20)
    def __str__ (self):
        return str(self.title)


# Payment
class Payment(models.Model):
    amount = models.FloatField(max_length=10)
    payment_type = models.ForeignKey(Payment_type, on_delete=models.CASCADE)
    date = models.DateField()
    

#  points
class Notes(models.Model):
    notetype = (
        ('پرداخت','پرداخت'),
        ('دریافت','دریافت')
    )
    name = models.CharField(max_length=50)
    whatfor = models.CharField(max_length=100)
    type = models.CharField(choices=notetype , max_length=50,default='pay')
    amount =models.FloatField()
    date = models.DateField(auto_now_add=True)
    