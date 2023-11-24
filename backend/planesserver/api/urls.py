from django.contrib import admin
from django.urls import path
from .views import CreateUserView, BalanceView, OpenedItemsView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView


app_name = 'api'
urlpatterns = [
    path('users/create/', CreateUserView.as_view()),
    path('users/login/', TokenObtainPairView.as_view()),
    path('users/refresh/', TokenRefreshView.as_view()),
    path('users/verify/', TokenVerifyView.as_view()),
    path('users/balance/', BalanceView.as_view()),
    path('users/items/', OpenedItemsView.as_view()),
    path('users/info/', UserInfoView.as_view())
]
