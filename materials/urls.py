from rest_framework.routers import SimpleRouter
from django.urls import path

from materials.views import CourseViewSet, LessonListAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonDestroyAPIView
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router= SimpleRouter()
router.register(prefix='', viewset=CourseViewSet, basename='course')

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(),name="lesson_list") ,
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(),name="lesson_retrive"),
    path("lesson/create", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
]

urlpatterns += router.urls