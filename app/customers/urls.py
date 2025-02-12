from customers import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.CustomerViewSet)

urlpatterns = router.urls
