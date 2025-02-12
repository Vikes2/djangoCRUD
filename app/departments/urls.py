from departments import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.DepartmentViewSet)

urlpatterns = router.urls
