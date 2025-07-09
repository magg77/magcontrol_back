from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.users_views import (RegisterView, ProfileView, LogoutView, UserUpdateView,
    ChangePasswordView,
    RequestPasswordResetView,
    PasswordTokenCheckView,
    SetNewPasswordView)
from users.views.customTokenObtainPairView import CustomTokenObtainPairView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'), # retorna access y refresh
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/<int:id>/update/', UserUpdateView.as_view(), name='update'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # recovery password
    path('auth/request-reset-password/', RequestPasswordResetView.as_view(), name='request-reset-password'),
    path('auth/password-reset/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('auth/set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]