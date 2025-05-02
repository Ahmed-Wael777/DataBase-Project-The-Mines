from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),

    path('home/',views.main_view,name='home'),
    path('update_patient/', views.update_patient, name='update_patient'),
    path('update_doctor/', views.update_doctor, name='update_doctor'),
]