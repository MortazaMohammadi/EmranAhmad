from django.contrib import admin
from .models import CustomUser, Employee, Payment_type, Payment,Notes,Pips_type,Pip

admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Payment_type)
admin.site.register(Payment)
admin.site.register(Notes)
admin.site.register(Pips_type)
admin.site.register(Pip)