from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(prefix="", viewset=UserViewSet, basename="course")

urlpatterns = []

urlpatterns += router.urls
