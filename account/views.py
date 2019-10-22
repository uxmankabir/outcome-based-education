from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'account/home.html', {})


def user_login(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plo_detail'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            context["user"] = user
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('plo_detail'))
        else:
            context["error_message"] = "Username or Password is incorrect."
            return render(request, 'account/home.html', context)
    else:
        return render(request, 'account/home.html', context)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('home'))


@login_required(login_url='home')
def password_change(request):
    return render(request, 'account/password_change.html', {})


def update_password(request):
    context = {}
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password1']

        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            return HttpResponseRedirect(reverse('password_change_done'))
        else:
            context['error_message'] = 'Please enter correct current password.'
            return render(request, 'account/password_change.html', context)

    return render(request, 'account/password_change.html', context)


def password_change_done(request):
    logout(request)
    return render(request, 'account/password_change_done.html', {})
