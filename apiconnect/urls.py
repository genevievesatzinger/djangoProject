
## URL files for apiconnect app

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
]

urlpatterns += staticfiles_urlpatterns()