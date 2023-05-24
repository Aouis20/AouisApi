from rest_framework.routers import DefaultRouter
from Accounts import views

router = DefaultRouter()

router.register(r"", views.UserViewSet)

urlpatterns = router.urls
