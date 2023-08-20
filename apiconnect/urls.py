
## URL files for apiconnect app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('results/', views.results, name='results'),
    path('cardresults/', views.cardResults, name='cardResults'),
    path('singleresult/<str:ntcId>/', views.singleResult, name='singleResult'),
]