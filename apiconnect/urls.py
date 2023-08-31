
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
    path('save_search/', views.save_search, name='save_search'),
    path('saved_searches/', views.saved_searches, name='saved_searches'),
    path('save_singleResult/', views.save_singleResult, name='save_singleResult'),
    path('saved_singleResults/', views.saved_singleResults, name='saved_singleResults'),
    path('saved/', views.saved, name='saved'),
    path('edit_profile/', views.saved, name='edit_profile'),
]