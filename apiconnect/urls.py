
## URL files for apiconnect app

from django.urls import path
from . import views
from .updateProfile import UpdateProfile

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_page, name="register"),
    path('results/', views.results, name='results'),
    path('card_results/', views.card_results, name='card_results'),
    path('single_result/<str:ntcId>/', views.single_result, name='single_result'),
    path('save_search/', views.save_search, name='save_search'),
    path('saved_searches/', views.saved_searches, name='saved_searches'),
    path('save_single_result/', views.save_single_result, name='save_single_result'),
    path('saved_single_results/', views.saved_single_results, name='saved_single_results'),
    path('saved/', views.saved, name='saved'),
    path('password-reset/', PasswordResetView.as_view(template_name='apiconnect/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='apiconnect/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='apiconnect/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='apiconnect/password_reset_complete.html'),name='password_reset_complete'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('updateprofile/', views.update_profile, name='update-profile'),
]