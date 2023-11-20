
## URL files for apiconnect app

from django.urls import path
from .updateProfile import UpdateProfile
from .views import main
from .views import authentication
from .views import results
from .views import save
from .views import profile
from .views import share
from .users.views import register, login_logout, profile


from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('home/', main.home, name='home'),
    path('', main.preloader, name='preloader'),
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
    #path('my_profile/', profile.my_profile, name='my_profile'),
    #path('updateprofile/', profile.update_profile, name='update-profile'),
    path('share_search/', share.share_search, name='share_search'),
    path('share_study/', share.share_study, name='share_study'),
    path('shared_search/search-id=<str:search_uid>/', share.shared_search, name='shared_search'),
    path('shared_study/study-id=<str:study_uid>/', share.shared_study, name='shared_study'),
    path('clinical_trial_info/', main.clinical_trial_info, name='clinical_trial_info'),

    path('login_hospital/', login_logout.login_hospital.as_view(), name='login_hospital'),
    path('login_doctor/', login_logout.login_doctor.as_view(), name='login_doctor'),
    path('login_patient/', login_logout.login_patient.as_view(), name='login_patient'),
    path('login_research_site/', login_logout.login_research_site.as_view(), name='login_research_site'),
    path('register_hospital/', register.register_hospital, name='register_hospital'),
    path('register_doctor/', register.register_doctor, name='register_doctor'),
    path('register_patient/', register.register_patient, name='register_patient'),
    path('register_research_site/', register.register_research_site, name='register_research_site'),
]