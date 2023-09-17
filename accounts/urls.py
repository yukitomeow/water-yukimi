from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            redirect_authenticated_user=True, template_name="accounts/login.html"
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),  # Adding the registration path
    path('i18n/', include('django.conf.urls.i18n')),

]
