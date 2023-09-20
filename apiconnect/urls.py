
## URL files for apiconnect app

from django.urls import path
from .updateProfile import UpdateProfile
from .views import main
from .views import authentication
from .views import results
from .views import save
from .views import profile
from .views import share


from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', main.home, name='home'),
    path('login/', authentication.login_page, name="login"),
    path('logout/', authentication.logout_user, name="logout"),
    path('register/', authentication.register_page, name="register"),
    path('search_results/', results.search_results, name='search-results'),
    path('card_results/', results.card_results, name='card_results'),
    path('single_result/<str:ntcId>/', results.single_result, name='single_result'),
    path('save_search/', save.save_search, name='save_search'),
    path('saved_searches/', save.saved_searches, name='saved_searches'),
    path('save_study/', save.save_study, name='save_study'),
    path('saved_studies/', save.saved_studies, name='saved_studies'),
    path('saved/', save.saved, name='saved'),
    path('password-reset/', PasswordResetView.as_view(template_name='apiconnect/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='apiconnect/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='apiconnect/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='apiconnect/password_reset_complete.html'),name='password_reset_complete'),
    path('my_profile/', profile.my_profile, name='my_profile'),
    path('updateprofile/', profile.update_profile, name='update-profile'),
    path('share_search/', share.share_search, name='share_search'),
    path('share_study/', share.share_study, name='share_study'),
    path('shared_search/search-id=<str:search_uid>/', share.shared_search, name='shared_search'),
    path('shared_study/study-id=<str:study_uid>/', share.shared_study, name='shared_study'),
]