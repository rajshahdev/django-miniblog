import re
from turtle import pos
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import Signupform, Loginform, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')

def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ip = request.session.get('ip',0)
        return render(request,'blog/dashboard.html',{'posts':post,'full_name':full_name,'groups':gps,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        messages.info(request,'you need to login')
        return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations for becoming an author!!! ')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
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


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = PostForm(request.POST)
            if post.is_valid():
                title = post.cleaned_data['title']
                desc = post.cleaned_data['desc']
                pst = Post(title=title,desc=desc)
                pst.save()
                post = PostForm()
                # return HttpResponseRedirect('/dashboard/')
        else:
            post = PostForm()
        return render(request,'blog/addpost.html',{'post':post})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            post = PostForm(request.POST,instance=pi)
            if post.is_valid:
                post.save()
        else:
            pi = Post.objects.get(pk=id)
            post = PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'post':post})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')