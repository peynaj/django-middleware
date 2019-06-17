from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.views import logout_then_login
from .utils import incr_wrong_try_count, get_wrong_try_data, max_try_count

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm()
        #print(form.is_valid())
        #if form.is_valid():
        username = request.POST['username']
        # check wrong try count
        try_c, try_ex = get_wrong_try_data(username)
        if try_c >= max_try_count:
            message = 'You tried {c} time by wrong data. You can not login until {ex}.'.format(
                c=try_c, ex=try_ex,
            )
            print(message)
            return render(request, 'login.html', {'form':form, 'show_message': True, 'message': message})

        raw_password = request.POST['password']
        print(username, raw_password)
        user = authenticate(username=username, password=raw_password)
        if raw_password is not None and user is None:
            print('a wrong try')
            try_c, _ = incr_wrong_try_count(username)
            message = 'You tried {try_c} time by wrong data. You can try to login only {rem_c} time.'.format(
                try_c=try_c, rem_c=max_try_count-try_c,
            )
            print(message)
            return render(request, 'login.html', {'form':form, 'show_message': True, 'message': message})
        else:
            login(request, user)
            return redirect('profile')
            
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form, 'show_message': False, 'message': ''})


def logoutview(request):
    return logout_then_login(request, login_url='login')

@login_required(login_url='/auth/login')
def profile(request):
    username = request.user.username
    context = 'Hello ' + username
    return render(request, 'profile.html', {'user': request.user})
