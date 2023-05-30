from rest_framework.routers import DefaultRouter
from Products import views

router = DefaultRouter()

router.register(r"", views.ProductViewSet)

urlpatterns = router.urls
