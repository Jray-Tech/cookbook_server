from . import views
from django.urls import path, include

urlpatterns = [
    path('login/', views.login, name='User-Login')
]

