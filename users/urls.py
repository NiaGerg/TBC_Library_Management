from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserCreate, user_profile, UserDetailAPIView, UserUpdateAPIView, CustomLoginView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='UserCreate'),
    path('profile/', user_profile, name='user-profile'),
    path('me/', UserDetailAPIView.as_view(), name='user-detail'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
