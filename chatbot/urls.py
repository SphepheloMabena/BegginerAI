from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import SaveFuelPriceView, HomeView, RegisterView, LoginView, ChatView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/', ChatView.as_view(), name='chat-view'),
    path('save_fuel_price/<str:fuel_type>/', SaveFuelPriceView.as_view(), name='save_fuel_price'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
