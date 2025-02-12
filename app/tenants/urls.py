from rest_framework import routers
from tenants import views

router = routers.DefaultRouter()
router.register(r"", views.TenantViewset)

urlpatterns = router.urls
