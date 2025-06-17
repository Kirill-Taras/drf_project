from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView, get_object_or_404,
)

from materials.models import Course, Lesson, Subscription
from materials.serializer import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from users.permissions import IsModer, IsOwner, IsOwnerOrModer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsModer | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Course.objects.none()
        if user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BaseLessonView:
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonCreateAPIView(CreateAPIView, BaseLessonView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView, BaseLessonView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModer | IsOwner)]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveUpdateAPIView(RetrieveAPIView, UpdateAPIView, BaseLessonView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonDestroyAPIView(DestroyAPIView, BaseLessonView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    """API для управления подписками на курсы"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Удаляем подписку если она существует
            subs_item.delete()
            message = 'Подписка удалена'
            subscription_status = False
        else:
            # Создаем новую подписку
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
            subscription_status = True

        return Response(
            {
                "message": message,
                "subscription_status": subscription_status,
                "course": course_item.title
            },
            status=status.HTTP_200_OK
        )