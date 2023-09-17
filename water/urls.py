from django.urls import path, include
from water import views

urlpatterns =[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('i18n/', include('django.conf.urls.i18n')),
]