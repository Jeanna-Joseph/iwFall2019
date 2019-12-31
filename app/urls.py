from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('student-registration/', views.studentregister, name='student-registration'),
    path('restaurant-registration/', views.restaurantregister, name='restaurant-registration'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('student/', views.studenthome, name='student-home'), 
#    path('studentsubmission/', views.studentsubmission, name='student-submission'),
#    path('restaurantsubmission/', views.restaurantsubmission, name='restaurant-submission'),
    path('restaurant/', views.restauranthome, name='restaurant-home'), 
    path('homepage/', views.homepage, name='homepage'),
]
