from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(prefix="users", viewset=UserViewSet, basename="users")
router.register(prefix="payments", viewset=PaymentViewSet, basename="payments")

urlpatterns = []

urlpatterns += router.urls
