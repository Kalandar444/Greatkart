# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import AccountSignUpForm

def signup(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = AccountSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically log the user in after signup
            if user.is_active:
                login(request, user)
                messages.success(request, "Account created successfully! Welcome!")
                
                # Redirect to homepage (front page)
                return redirect(next_url or '/')

            messages.info(request, "Please activate your account.")
            return redirect('login')

    else:
        form = AccountSignUpForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
        'next': next_url
    })
