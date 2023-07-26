
## URL files for apiconnect app

from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
    # path('sign_in/', views.sign_in, name='sign in')
]

urlpatterns += staticfiles_urlpatterns()