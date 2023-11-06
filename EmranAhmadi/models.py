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
    
class Pips_type(models.Model):
    title = models.CharField(max_length=30)
    country = models.CharField(max_length=20)

class Pip(models.Model):
    name = models.CharField(max_length=30)
    piptype = models.ForeignKey(Pips_type, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    inch = models.CharField(max_length=10)
    wieght = models.FloatField(default=0)

class BuyMatrial(models.Model):
    piptype = models.ForeignKey(Pips_type, on_delete=models.CASCADE)
    wieght = models.FloatField(default=0)
    price = models.FloatField(default=0)
    company = models.CharField(max_length= 50)
    date = models.DateField(auto_now=True)

class Bill(models.Model):
    customer = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    total = models.FloatField()
    date = models.DateField(auto_now=True)
    done = models.BooleanField(default=False)
    
class SellPip(models.Model):
    pip = models.ForeignKey(Pip, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    totalprice = models.FloatField(default = 0)
