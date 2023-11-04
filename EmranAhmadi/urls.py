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
    # path('', home_page),

 
]
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
