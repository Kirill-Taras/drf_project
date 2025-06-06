from rest_framework.serializers import ModelSerializer
from users.models import User, Payment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["phone", "city", "avatar"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UsersDetailSerializer(ModelSerializer):
    payment = PaymentSerializer()

    class Meta:
        model = User
        fields = ("phone", "city", "avatar", "payment")