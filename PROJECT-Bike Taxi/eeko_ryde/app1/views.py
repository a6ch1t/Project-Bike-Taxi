from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from app1.models import *
from .form import *

# Create your views here.

from .models import *
from app1.form import *

def index(request):
    return render(request,'index.html')

def service(request):
    return render(request,'service.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')




def signup(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('pass1')
        password2=request.POST.get('pass2')
        if password1==password2:
            if User.objects.filter(username=username,email=email).exists():
                messages.info(request,'useername already exists!')
                print("Already Have")
                return redirect(signup)
            else:
                new_user=User.objects.create_user(username,email,password1)
                new_user.save()
                return redirect(user_login)
        else:
            print("wrong Password")
    return render(request,'signup.html')
    

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('pass1')
        user=authenticate(request,username=username,password=password1)
        if user is not None:
            login(request,user)
            return redirect(index)
        else:
            messages.info(request,'user not exist')
            print('user not exist')
            return redirect(user_login)
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect(user_login)

def cart(request):
    l=Locate.objects.all()
    return render(request,'cart.html',{'locate':l})

def checkoute(request):
    l=Locate.objects.all()
    if request.method=='POST':
        starting=request.POST.get('start')
        reaching=request.POST.get('ends')
        type1=request.POST.get('Normal')
        type2 =request.POST.get('ev')
        ty1='PASSION PRO(eEko Petrol ByKE)'
        ty2='OLA(eEko EV. ByKE'
        a1=Locate.objects.get(location=starting)
        b=a1.id
        a2=Locate.objects.get(location=reaching)
        b2=a2.id
        print(type1,type2)
        if type1 is not None:
            if b < b2:
                c=b2-b
                charge=c*15
                rydinfo= rydeinfo.objects.create(starting_location=starting, ending_location=reaching, typey=ty1, price=charge, user=request.user)
                rydinfo.save()
                return redirect(byke)
            elif b2 < b:
                c=b-b2
                charge=c*15
                rydinfo= rydeinfo.objects.create(starting_location=starting, ending_location=reaching, typey=ty1, price=charge, user=request.user)
                rydinfo.save()
                return redirect(byke)
            else:
                return redirect(checkoute)
        elif type2 is not None:
            if b < b2:
                c=b2-b
                charge=c*17
                rydinfo= rydeinfo.objects.create(starting_location=starting, ending_location=reaching, typey=ty2, price=charge, user=request.user)
                rydinfo.save()
                return redirect(byke)
            elif b2 < b:
                c=b-b2
                charge=c*17
                rydinfo= rydeinfo.objects.create(starting_location=starting, ending_location=reaching, typey=ty2, price=charge, user=request.user)
                rydinfo.save()
                return redirect(byke)
            else:
                return redirect(checkoute)
        else:
            return redirect(checkoute)
        
    return render(request,'forme.html',{'locate':l})
def byke(request):
    inf = rydeinfo.objects.all().order_by('-id').first()
    return render(request,'successful.html',{'information':inf})

