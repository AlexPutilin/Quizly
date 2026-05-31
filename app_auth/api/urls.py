from django.urls import path
from .views import RegisterView, LoginTokenView, LogoutView, RefreshTokenView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]