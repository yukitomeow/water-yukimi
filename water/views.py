from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from water.models import WaterConsumption
from accounts.models import UserProfile
from water.forms import WaterConsumptionForm
from django.db.models import Sum
from datetime import date
from django.http import HttpResponseForbidden
from collections import defaultdict
from calendar import monthrange
from django.utils.translation import gettext as _
from django.contrib import messages

from django.utils.dateformat import DateFormat
from django.utils import translation


@login_required
def top(request, ):
    today = date.today()
    print(today)
    current_language = translation.get_language()
    
    if current_language == "en":
        formatted_today = today.strftime('%b. %d, %Y')  # This will give "Sept. 2, 2023" for English
    elif current_language == "ja":
        formatted_today = today.strftime('%Y年%m月%d日')  # This will give "2023年9月2日" for Japanese
    else:
        formatted_today = today.strftime('%Y-%m-%d') 
    
    date_string = _("Your water intake for {formatted_today} is")
    translated_date = date_string.format(formatted_today=formatted_today)
    username = request.user.username
    # Ensure the logged-in user can only see their records
    if request.user.username != username:
        return HttpResponseForbidden("You don't have permission to view this.")

    


    today_record = WaterConsumption.objects.filter(user=request.user, date=today).first()
    today_record_id = today_record.id if today_record else None

    # Retrieve today's total water consumption for the user
    water_today = (
        WaterConsumption.objects.filter(user=request.user, date=today).aggregate(
            total=Sum("amount_drank")
        )["total"]
        or 0
    )

    userprofile = UserProfile.objects.filter(user=request.user).first()
    unit = userprofile.unit if userprofile and userprofile.unit else 'ml'
    if request.method == "POST":
        form = WaterConsumptionForm(request.POST)
        if form.is_valid():
            water = form.save(commit=False)
            water.user = request.user
            water.date = today  # set today's date
            water.save()

            # Recalculate the water consumed today after saving the new record
            water_today = (
                WaterConsumption.objects.filter(
                    user=request.user, date=today
                ).aggregate(total=Sum("amount_drank"))["total"]
                or 0
            )
    title_string=_("Welcome {username}!")
    translated_title= title_string.format(username=username, )

  


    form = (
        WaterConsumptionForm()
    )  
    strings_to_translate = [
        "Water Consumption Log",
        "Water Consumption for Today", 
        "Username", 
        "Date",
        "Total Water Consumed Today",
        "Go to Dashboard",
        "Add Water Consumption",
        ]
    for string in strings_to_translate:
        translated_string = _(string)
        messages.add_message(request, messages.SUCCESS, translated_string)

    context = {
        "total_water_today": water_today,
        "username": username,
        "date": today,
        "form": form,
        "unit":unit,
        "record_id": today_record_id,
        'translated_title': translated_title,
        'translated_date':translated_date,
        
    }

    return render(request, "water/top.html", context)


@login_required
def dashboard(request):
    username = request.user.username
    current_date = date.today()
   
    df = DateFormat(current_date)
    current_month_abbr = df.format('M')  
    current_year = df.format('Y')
    user_water_records = WaterConsumption.objects.filter(user=request.user, date__month=current_date.month)
    userprofile = UserProfile.objects.filter(user=request.user).first()
    unit = userprofile.unit if userprofile and userprofile.unit else 'ml'
   
    daily_consumption = defaultdict(float)
    for record in user_water_records:
        daily_consumption[record.date.day] += record.amount_drank

    total_consumption = sum(daily_consumption.values())
    days_in_month = monthrange(current_date.year, current_date.month)[1]
    average_consumption_per_day = round(total_consumption / days_in_month)


    
    title_string = _("Welcome back {username} !")
    translated_title = title_string.format(username=username, )

      
    average_prefix_string = _("Your average water intake for {month} {year} is ")
    average_value_string = _("{average} {unit}")
        
    translated_average_prefix = average_prefix_string.format(month=current_month_abbr, year=current_year)
    translated_average_value = average_value_string.format(average=average_consumption_per_day, unit=unit)


    amount_consumed_string = _("Amount Consumed")

    
    context = {
        "username":username,
        'current_month_abbr':current_month_abbr,
        'daily_consumption': sorted(daily_consumption.items()),
        'unit':unit,
        'current_year':current_year,
        'average_consumption_per_day':average_consumption_per_day,
        'translated_title': translated_title,
        'translated_average_prefix': translated_average_prefix,
        'translated_average_value': translated_average_value,
        'amount_consumed': amount_consumed_string,
    }
    return render(request, 'water/dashboard.html', context)


