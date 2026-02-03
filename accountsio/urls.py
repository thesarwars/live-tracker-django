from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Login endpoint: returns access and refresh tokens
    path("/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Optional: refresh endpoint to get a new access token
    path("/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
