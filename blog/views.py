from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import Signupform, Loginform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')

def dashboard(request):

    return render(request,'blog/dashboard.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations for becoming an author!!! ')
            form.save()
            form = Signupform()
    else:
        form = Signupform()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = Loginform(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']    
                pword = form.cleaned_data['password']
                user = authenticate(username=uname,password=pword)
                if user is not None:
                    login(request,user)
                    messages.success(request,"loggin successfully!!!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = Loginform()
    else:
        return HttpResponseRedirect('/dashboard/')
    return render(request,'blog/login.html',{'form':form})