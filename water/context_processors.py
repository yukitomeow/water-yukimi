from django.contrib import messages
from django.utils.translation import gettext as _

def translated_message(request):
    # Translate the message
    strings_to_translate = [
        "Water Consumption",
        "Dashboard", 
        "Logout",
        "Login", 
        "Register",
        "言語変更",
        "英語",
        "JP",
        "Submit",
        "Amount drank"
        ]
    for string in strings_to_translate:
        translated_string = _(string)
        messages.add_message(request, messages.SUCCESS, translated_string)
    
    # Return an empty dictionary, as we don't need to pass additional context
    return {}
