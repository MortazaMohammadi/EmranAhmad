from django.urls import path
from django.conf.urls.static import static
from EmranAhmad import settings
from .views import *
urlpatterns =[

    path('', loginPage, name='loginPage'),
    path('logout' , logout_user),
    path('addPayment', addPayment, name='addPayment'),
    path('paymentList', paymentList, name='paymentList'),
    
    path('employeeRegister', employeeRegister, name = 'employeeRegister'),
    path('employeeUpdate/<int:user_id>/', employeeUpdate, name = 'employeeUpdate'),
    path('notes',notes,name = 'notes'),
    path('addpip',addpip, name ='addpip'),
    path('updatepip/<int:pip_id>/',updatepip,name = 'updatepip'),  
    path('deletepip/<int:pip_id>/', deletepip, name = 'deletepip'),
    path('buymatrial', buymatrial, name = 'buymatrial'),
    path('updatematrial/<int:matrial_id>/',updatematrial, name = 'updatematrial'),
    path('deletematrial/<int:matrial_id>/',deletematrial,name='deletematrial'),
    path('addbill',addbill, name='addbill'),
    path('updatebill/<int:bill_id>/', updatebill, name= 'updatebill'),
    path('deletebill/<int:bill_id>/', deletebill, name = 'deletebill'),
    path('billdone/<int:bill_id>/',billdone, name = 'billdone'),
    path('donebilllisting', donebilllisting, name ='donebilllisting'),
    path('printbill/<int:bill_id>/',printbill,name='printbill'),
    path('sellpip/<int:bill_id>/',sellpip,name = 'sellpip'),
    path('updatesellpip/<int:sellpip_id>/', updatesellpip,name = 'updatesellpip'),
    path('deletesellpip/<int:sellpip_id>/',deletesellpip,name = 'deletesellpip'),
    
    # path('', home_page),

 
]
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
