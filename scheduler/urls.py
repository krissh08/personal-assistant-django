# scheduler/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # The root URL will now be the public homepage
    path('', views.home, name='home'),
    
    # The dashboard is now at its own private URL
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='scheduler/login.html'), name='login'),
    
    # After logging out, send the user to the new public homepage
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]