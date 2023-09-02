
## URL files for apiconnect app

from django.urls import path
from . import views

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('results/', views.results, name='results'),
    path('cardresults/', views.cardResults, name='cardResults'),
    path('singleresult/<str:ntcId>/', views.singleResult, name='singleResult'),
    path('save_search/', views.save_search, name='save_search'),
    path('saved_searches/', views.saved_searches, name='saved_searches'),
    path('save_singleResult/', views.save_singleResult, name='save_singleResult'),
    path('saved_singleResults/', views.saved_singleResults, name='saved_singleResults'),
    path('saved/', views.saved, name='saved'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password-reset/', PasswordResetView.as_view(template_name='apiconnect/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='apiconnect/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='apiconnect/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='apiconnect/password_reset_complete.html'),name='password_reset_complete'),
]