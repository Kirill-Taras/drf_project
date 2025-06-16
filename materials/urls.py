from rest_framework.routers import SimpleRouter
from django.urls import path

from materials.views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonRetrieveUpdateAPIView,
)
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register(prefix="", viewset=CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveUpdateAPIView.as_view(), name="lesson_retrive"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
]

urlpatterns += router.urls
