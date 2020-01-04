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
    #new
    path('submit-story/<int:pk>/', views.submitstory, name='submit-story'), 
    #new
    path('submit-post/<int:pk>/', views.submitpost, name='submit-post'), 
    path('redeemable-rewards/', views.redeemablerewards, name='redeemable-rewards'),
    path('redeem-story/<int:pk>/', views.redeemstory, name='redeem-story'), 
    path('redeem-post/<int:pk>/', views.redeempost, name='redeem-post'),
    path('restaurant/', views.restauranthome, name='restaurant-home'), 
    path('restaurant-story/', views.restaurantstory, name='restaurant-story'), 
    path('restaurant-post/', views.restaurantpost, name='restaurant-post'), 
    path('view-submissions/', views.viewsubmissions, name='view-submissions'), 
    path('account-details/', views.accountdetails, name='account-details'), 
    path('homepage/', views.homepage, name='homepage'),
]
