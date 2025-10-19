from django.shortcuts import render,redirect
from .models import Task
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

# Create your views here.

login_required(login_url='login')
def list_tasks(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request,"tasks/task_list.html",{"tasks":tasks})

login_required(login_url='login')
def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        Task.objects.create(user = request.user,title=title,description=description)
        messages.success(request,"Task created successfully...")
        return redirect("task_list")
    return render(request,"tasks/forms.html")

login_required(login_url='login')
def update_task(request,pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.completed = "completed" in request.POST
        task.save()
        messages.success(request,"Task updated successfully...")
        return redirect("task_list")
    return render(request,"tasks/forms.html")

login_required(login_url='login')
def delete_task(request,pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request,"Task Deleted successfully...")
        return redirect("task_list")
    return render(request,"tasks/task_confirm_delete.html",{"task":task})


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request,"Password do not match...")
            return redirect("signup")
        
        if User.objects.filter(username = username).exists():
            messages.error(request,"username already taken...")
            return redirect("signup")
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        messages.success(request,"User Created successfully...")
        return redirect("task_list")
    return render(request,"tasks/auth.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"User Logined successfully...")
            return redirect("task_list")
        else:
            messages.error(request, "❌ Invalid credentials.")
            return redirect("login")
    return render(request,"tasks/auth.html")

def logout_view(request):
    logout(request)
    messages.info(request,"Logged out successfully...")
    return redirect("login")
