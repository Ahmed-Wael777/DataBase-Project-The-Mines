from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('update_patient/', views.update_patient, name='update_patient'),
    path('update_doctor/', views.update_doctor, name='update_doctor'),
]