from rest_framework.routers import DefaultRouter
from Categories import views

router = DefaultRouter()

router.register(r"", views.CategoryViewSet)

urlpatterns = router.urls
