from django.shortcuts import render, redirect
from .forms import RegistrationForm
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from django.contrib import messages






@login_required
def redirect_to_user_profile(request):
    # Redirect to the logged in user's profile page
    return redirect(f"/{request.user.username}/")



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user, unit=form.cleaned_data['unit'])
            profile.save()

            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('top')

    else:
        form = RegistrationForm()

    strings_to_translate = [
        "Water Consumption Log",
        "Water Consumption for Today", 
        "Username", 
        "Date",
        "Total Water Consumed Today",
       
        "Add Water Consumption",
        ]
    for string in strings_to_translate:
        translated_string = _(string)
        messages.add_message(request, messages.SUCCESS, translated_string)

    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)

