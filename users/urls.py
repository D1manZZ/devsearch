from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', developers, name='developers'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('<int:pk>/', profile, name='profile'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('messages/', messages_list, name='messages'),
    path('messages/<int:pk>', send_message, name='send_message'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='users/reset_password.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/reset_password_done.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/reset_password_complete.html'), name='password_reset_complete')
]
