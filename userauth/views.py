from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Account


# ================= LOGIN =================
def login_user(request):
    # If already logged in → go home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("LOGIN TRY:", username, password)

        # Try username login
        user = authenticate(request, username=username, password=password)

        # Try email login
        if user is None:
            try:
                user_obj = Account.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except Account.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password")

    context = {
        'is_login': 1,
    }
    return render(request, 'userauth/login.html', context)


# ================= SIGNUP =================
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        data = request.POST

        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        if password == password2:
            if Account.objects.filter(username=username).exists():
                messages.info(request, 'Username not available. Use another username.')
                return redirect('userauth:signup')

            elif Account.objects.filter(email=email).exists():
                messages.info(request, 'Email not available. Use another email.')
                return redirect('userauth:signup')

            else:
                user = Account.objects.create_user(
                    name=name,
                    username=username,
                    email=email,
                    password=password
                )
                user.save()

                messages.success(request, 'Account created successfully. Please login.')
                return redirect('userauth:login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('userauth:signup')

    context = {
        'is_login': 0,
    }
    return render(request, 'userauth/signup.html', context)


# ================= LOGOUT =================
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

