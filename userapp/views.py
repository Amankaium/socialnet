from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def registration(request):
    if request.method == "POST":
        password_1 = request.POST["password_1"]
        password_2 = request.POST["password_2"]
        if password_1 != password_2:
            messages.error(request, "Пароли не совпадают")
        else:
            user = User(
                username=request.POST["login"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
            )
            user.set_password(password_1)
            user.save()
            messages.success(request, "Вы успешно прошли регистрацию!")
            return redirect("/") 
    
    return render(request, 'userapp/registration.html')


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request=request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'userapp/sign_in.html')


def sign_out(request):
    logout(request)
    return redirect('/')
