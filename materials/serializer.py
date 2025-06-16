from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для вывода информации об уроках."""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "lessons_count"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ("title", "description", "count_lessons", "lessons")

    def get_count_lessons(self, obj):
        return obj.lessons.count()
