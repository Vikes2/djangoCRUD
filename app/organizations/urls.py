from organizations import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.OrganizationViewSet)

urlpatterns = router.urls
