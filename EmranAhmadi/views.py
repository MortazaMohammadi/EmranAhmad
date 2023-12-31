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
