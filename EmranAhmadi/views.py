import array
from django.shortcuts import render
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout , authenticate , update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import Http404 , HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from EmranAhmadi.EmailBackEnd import EmailBackEnd
from EmranAhmadi import models as mod
from django.db.models import Sum
from django.contrib import messages

# Login user_account view
def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(
            request, username=user_name, password=password)
        if user != None:
            login(request, user)
            try:
                bill = mod.Bill.objects.get(id = 50)
            except:
                bill = None
            if bill != None:
                return redirect('/logout')
            else:
                 return redirect('/bill')
        else:
            context['aut']= 'نام کاربری یا رمز عبور تان اشتباه است.'
    return render(request, 'account/login.html',context)

# logout
def logout_user(request):
    logout(request)
    return redirect('/')

# add payments
@login_required(login_url='/')
def addPayment(request):    
    context = {}
    if request.method == 'POST':
        paymodel = mod.Payment()
        paymodel.amount= request.POST.get('amount_txt')
        paytype = request.POST.get('ptype_txt')
        paymodel.payment_type = mod.Payment_type.objects.get(id = paytype)
        paymodel.date = request.POST.get('date_txt')
        paymodel.save()
        return redirect('/addPayment')
    else:
        context['ptype'] = mod.Payment_type.objects.all()
        context['page'] = 'اضافه مصرف'
        context['list'] = mod.Payment.objects.all()
        context['addpay'] = ' text-warning sub-bg ps-3'
        return render(request, 'office/addPayment.html',context)

# payment list and static for payment
@login_required(login_url='/')
def paymentList(request):
    context = {}
    if request.method == 'GET':
         Fptype = request.GET.get('ptype_txt')
         if Fptype:
           if Fptype == '0':
               context['records'] = mod.Payment.objects.all()
           else:
                 ptype = mod.Payment_type.objects.get(id=Fptype)  # Use get() instead of filter()
                 context['records'] = mod.Payment.objects.filter(payment_type=ptype.id)
         else:
              context['records'] = mod.Payment.objects.order_by('-id') 
    total_amount = mod.Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    if total_amount:
        paytype = mod.Payment_type.objects.all()
        context['total_amount'] = total_amount
        if paytype:
            l1 = []
            
            for i in paytype: 
                l2 = []
                i.title
                try:
                    filtered_amount = mod.Payment.objects.filter(payment_type__id=i.id).aggregate(filtered_amount=Sum('amount'))['filtered_amount']
                    if filtered_amount ==None:
                        filtered_amount =0
                except TypeError:
                    filtered_amount = 1
                l2.append(i.title)
                l2.append(filtered_amount)
                l2.append(round(filtered_amount*100/total_amount,2))
                l1.append(l2)
            context['eachptype'] = l1
            context['paytype'] = mod.Payment_type.objects.all()
    context['page'] = 'لیست مصارف'
    context['listpay'] = ' text-warning sub-bg ps-3'
    return render(request, 'office/paymentList.html',context)
# employee register
@login_required(login_url='/')
def employeeRegister(request): 
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lname = request.POST.get('lname_txt')
        if 'profile_img' in request.FILES:
            profileImage = request.FILES['profile_img']
        else:
            profileImage = None
        phone = request.POST.get('phone_txt')
        address = request.POST.get('address_txt')
        email = request.POST.get('email_txt')
        username = request.POST.get('username_txt')
        password = request.POST.get('password1_txt')
        repassword = request.POST.get('password2_txt')
        if password == repassword:
            if mod.CustomUser.objects.filter(email=email).exists():
                context['email_error'] = 'email is already exists'
                print('email is already exists')
                return render(request, 'account/employee_registeration.html', context)
            else:
                username = username.lower()
                user = mod.CustomUser.objects.create_user(
                    username=username, email=email, password=password)
                user.first_name = name
                user.last_name = lname
                user.profile_image = profileImage
                user.save()
                Employee_obj = mod.Employee(
                        admin=user,
                        phone=phone,
                        address = address,
                    )
                Employee_obj.save()
        else:
            context['password_error'] = 'Password is not match'
            print('password mismatch')
            return render(request, 'account/employee_registeration.html', context)
    context['page'] = 'راجستر کارمند'
    
    return render (request, 'account/employee_registeration.html')

# Notes  
@login_required(login_url='/')
def notes(request):
    context = {}
    
    context['money'] = mod.Money.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        whatfor = request.POST.get('whatfor_txt')
        type = request.POST.get('type_txt')
        amount = request.POST.get('amount_txt')    
        note = mod.Notes(
            name = name,
            whatfor = whatfor,
            type = type,
            amount = amount,
        )
        note.save()
        return redirect('notes')
    
    context['records'] = mod.Notes.objects.all()
    if request.method == 'GET':
        any = request.GET.get('any_txt')
        mytype = request.GET.get('type_txt')
        if mytype == 'همه':
            result = mod.Notes.objects.filter(Q(whatfor__icontains=any) | Q(name__icontains=any) | Q(amount__icontains=any) | Q(date__icontains=any) )
        elif mytype == None:
            result = mod.Notes.objects.all()
        else:
            result = mod.Notes.objects.filter(Q(whatfor__icontains=any) | Q(name__icontains=any) | Q(amount__icontains=any) | Q(date__icontains=any) ,type = mytype)
        context['records'] = result
    
    context['notes'] = ' text-warning sub-bg ps-3'
    return render(request, 'note/notes.html',context)


# profile update
def employeeUpdate(request,user_id):  
    context = {}
    context['money'] = mod.Money.objects.all()
    customuser = mod.CustomUser.objects.get(id = user_id)
    myuser = None
    
    try:
        if mod.Boss.objects.get(admin = customuser):
            myuser = mod.Boss.objects.get(admin = customuser)
        elif mod.Employee.objects.get(admin = customuser):
            myuser = mod.Employee.objects.get(admin = customuser)
        else:
            myuser = mod.Manager.objects.get(admin = customuser)
    except:
        pass
    context['myuser'] = myuser
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lname = request.POST.get('lname_txt')
        if 'profile_img' in request.FILES:
            profileImage = request.FILES['profile_img']
        else:
            profileImage = None
        phone = request.POST.get('phone_txt')
        address = request.POST.get('address_txt')
        email = request.POST.get('email_txt')
        username = request.POST.get('username_txt')
        cupassword = request.POST.get('password0_txt')
        password = request.POST.get('password1_txt')
        repassword = request.POST.get('password2_txt')
        user = authenticate(username=request.user.username,
                            password=cupassword)
        if user is None:
            messages.error(request, 'Current password is incorrect')
            return redirect('/employeeUpdate/'+ str(user_id))
        else:
            if password != repassword:
                messages.error(
                    request, 'new password and confirm password is does not match')
                return redirect('/employeeUpdate/'+ str(user_id))
            else:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
               

            user.first_name = name
            user.last_name = lname
            if profileImage:
                user.profile_image.delete()
                user.profile_image = profileImage
            else:
                pass
            user.email = email
            user.username = username
            user.save()
            myuser.phone = phone
            myuser.address = address
            myuser.save()
            return redirect('/bill')
    context['page'] = 'آپدیت کارمند'
    return render(request, 'account/employee_update.html',context)

def addpip(request):
    context={}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        piptype = request.POST.get('piptype_txt')
        inch = request.POST.get('inch_txt')
        wieght = request.POST.get('wieght_txt')
        price = request.POST.get('price_txt')
        pip = mod.Pip(
            name = name,
            piptype = mod.Pips_type.objects.get(id = piptype),
            inch = inch,
            wieght = wieght,
            price = price
        )
        pip.save()
        return redirect('/addpip')
    context['piptypes'] = mod.Pips_type.objects.all()
    context['pipslisting'] = mod.Pip.objects.all()
    context['page'] = 'اضافه محصول'
    context['addpip'] = 'sub-bg text-warning'
    return render(request,'pip/addpip.html',context)

def updatepip(request,pip_id):
    context={}
    context['pip'] = mod.Pip.objects.get(id = pip_id)
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        piptype = request.POST.get('piptype_txt')
        inch = request.POST.get('inch_txt')
        wieght = request.POST.get('wieght_txt')
        price = request.POST.get('price_txt')
        pip = mod.Pip.objects.get(id = pip_id)
        pip.name = name
        pip.piptype = mod.Pips_type.objects.get(id = piptype)
        pip.inch = inch
        pip.wieght = wieght
        pip.price = price
        pip.save()
        return redirect('/addpip')
    context['pipslisting'] = mod.Pip.objects.all()
    context['piptypes'] = mod.Pips_type.objects.all()
    context['page'] = 'ویرایش محصول'
    context['addpip'] = 'sub-bg text-warning'
    return render(request,'pip/updatepip.html',context)

def deletepip(request,pip_id):
    pip = mod.Pip.objects.get(id = pip_id)
    pip.delete()
    return redirect('/addpip')


def buymatrial(request):
    context={}
    if request.method == 'POST':
        piptype = request.POST.get('piptype_txt')
        wieght = request.POST.get('wieght_txt')
        price = request.POST.get('price_txt')
        company = request.POST.get('compay_txt')
        matrial = mod.BuyMatrial(
            piptype = mod.Pips_type.objects.get(id = piptype),
            wieght = wieght,
            price = price,
            company = company
        )
        matrial.save()
    context['page'] = 'مواد اولیه'
    context['buymatrial'] = 'sub-bg text-warning'
    context['piptypes'] = mod.Pips_type.objects.all()
    matriallisting = mod.BuyMatrial.objects.order_by('-id')
    context['matriallisting'] = matriallisting
    return render(request, '/matrials/buymatrial.html',context)

def updatematrial(request,matrial_id):
    context={}
    context['matrial'] = mod.BuyMatrial.objects.get(id = matrial_id)
    if request.method == 'POST':
        piptype = request.POST.get('piptype_txt')
        wieght = request.POST.get('wieght_txt')
        price = request.POST.get('price_txt')
        company = request.POST.get('compay_txt')
        matrial = mod.BuyMatrial.objects.get(id = matrial_id)
        matrial.piptype = mod.Pips_type.objects.get(id = piptype)
        matrial.wieght = wieght
        matrial.price = price
        matrial.company = company
        matrial.save()
        return redirect('/buymatrial')
    context['page'] = 'ویرایش مواد'
    context['buymatrial'] = 'sub-bg text-warning'
    context['piptypes'] = mod.Pips_type.objects.all()
    return render(request,'matrial/updatematrial.html',context)

def deletematrial(request,matrial_id):
    matrial = mod.BuyMatrial.objects.get(id = matrial_id)
    matrial.remove()
    redirect('/buymatrial')

def addbill(request):
    context = {}
    if request.method =='POST':
        customer = request.POST.get('customer_txt')
        address = request.POST.get('address_txt')
        bill = mod.Bill(
            customer = customer,
            address = address,
        )
        bill.save()
        return redirect('/sellpip'+ str(bill.id))
    try:
        billlisting = mod.Bill.objects.filter(active = False).order_by('-id')
    except:
        pass
    if billlisting == None:
        context['none'] = 'هیج بِلی در جریان نیست'
    else:
        context['billlisting'] = billlisting
    context['page'] = 'ایجاد بل'
    context['addbill'] = 'sub-bg text-warning'
    return render (request,'/sell/addbill.html',context)

def updatebill(request,bill_id):
     context = {}
     context['bill'] = mod.Bill.objects.get(id = bill_id)
     if request.method =='POST':
        customer = request.POST.get('customer_txt')
        address = request.POST.get('address_txt')
        bill = mod.Bill.objects.get(id = bill_id)
        bill.customer = customer
        bill.address = address
        bill.save()
        return redirect('/addbill')
     context['page'] = 'ویرایش بل'
     context['addbill'] = 'sub-bg text-warning'
     return render(request,'/sell/updatebill.html',context)


def deletebill(requext, bill_id):
    bill = mod.Bill.objects.get(id - bill_id)
    bill.remove()
    return redirect('/addbill')

def billdone(request,bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    bill.done = True
    bill.save()
    return redirect('/addbill')
 
def donebilllisting(request):
    context = {}
    if request.method == 'GET':
       billsearch =  request.POST.get('search_txt')
       if billsearch == None:
           context['billlisting'] = mod.Bill.objects.filter(done = True)
       else:
           try:
               context['billlisting'] = mod.Bill.objects.get(id = billsearch, done = True)
           except:
               context['none'] = 'هیج بِلی پیدا نشد'
       return redirect('donebilllisting')
    context['page'] = 'بل های ثبت شده'
    context['donebilllisting'] = 'sub-bg text-warning'
    return render(request,'sell/donebilllisting.html',context)
def printbill(request,bill_id):
    context = {}
    context['page'] ='پرنت بل'
    bill = mod.Bill.objects.get(id = bill_id)
    context['sellpips'] = mod.SellPip.objects.filter(bill = bill)
    context['total'] = mod.SellPip.objects.aggregate(total_amount=Sum('pip__price'))['total_amount']
    return render(request,'/sell/printbill.html',context)

# next plane :

def sellpip(request,bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    try:
        sells = mod.SellPip.objects.filter(bill = bill)
    except:
        pass
    context = {}
    context['bill'] = bill
    context['sells'] = sells
    context['pips'] = mod.Pip.objects.all()
    if request.method == 'POST':
        pip = request.POST.get('pip_txt')
        amount = request.POST.get('amount_txt')
        mypip = mod.Pip.objects.get(id = pip),
        mysellpip = mod.SellPip(
            pip = mypip,
            bill = bill,
            amount = amount,
            totalprice = float(amount) * float(mypip.price)
        )
        mysellpip.save()
        return redirect('/sellpip/'+ str(bill_id))
    context['page'] = 'بل'
    context['addbill'] = 'sub-bg text-warning'
    return render(request, '/sell/sellpip.html',context)

def updatesellpip(request,sellpip_id):
    context = {}
    if request.method == 'POST':
        pip = request.POST.get('pip_txt')
        amount = request.POST.get('amount_txt')
        mypip = mod.Pip.objects.get(id = pip),
        mysellpip = mod.SellPip.objects.get(id = sellpip_id)
        mysellpip.pip = mypip,
        mysellpip.amount = amount,
        mysellpip.totalprice = float(amount) * float(mypip.price)
        mysellpip.save()
        return redirect('/sellpip/'+ str(mysellpip.pip.id))
    context['page'] = 'ویرایش مواد'
    context['addbill'] = 'sub-bg text-warning'
    return render(request,'sell/updatesellpip.html')
def deletesellpip(request,sellpip_id):
    sellpip = mod.SellPip.objects.get(id = sellpip)
    sellpip.remove()
    return redirect('/sellpip'+ str(sellpip.bill.id))
 
# def statistic(request):
#     # total payment
#     # total matrials
#     # total Bill
#     # tottal bill -payment - matrials
#     pass