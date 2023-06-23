from django.contrib import admin
from django.urls import path, include
from Accounts.views import TokenObtainViewSet, TokenVerifyViewSet
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/token/", TokenObtainViewSet.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "auth/verify/", TokenVerifyViewSet.as_view({"get": "get"}), name="token_verify"
    ),
    path("accounts/", include("Accounts.urls")),
    path("categories/", include("Categories.urls")),
    path("products/", include("Products.urls")),
    path("transactions/", include("Transactions.urls")),
]
