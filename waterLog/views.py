from django.shortcuts import redirect
from django.utils import translation

def redirect_to_language(request):
    language = translation.get_language_from_request(request)
    if language not in ['en', 'ja']:
        language = 'en'
    return redirect(f'/{language}/')
