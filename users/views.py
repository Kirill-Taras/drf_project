from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from materials.models import Course
from users.filters import PaymentFilter

from users.models import User, Payment
from users.permissions import IsOwner
from users.serializer import (
    UserRegisterSerializer,
    UserSerializer,
    PaymentSerializer,
    UserDetailSerializer,
)
from users.services import StripeService


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "create":
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.none()
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        payment.save()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)

            # Создаем продукт и цену в Stripe
            product_id = StripeService.create_product(course.title)
            price_id = StripeService.create_price(course.price, product_id)

            # Создаем сессию оплаты
            session_data = StripeService.create_checkout_session(price_id)

            # Сохраняем платеж в БД
            payment = Payment.objects.create(
                user=request.user,
                paid_course=course,
                amount=course.price,
                stripe_product_id=product_id,
                stripe_price_id=price_id,
                stripe_session_id=session_data['session_id'],
                payment_link=session_data['payment_link'],
                payment_method="transfer"
            )

            return Response({
                'payment_id': payment.id,
                'payment_link': payment.payment_link
            }, status=status.HTTP_201_CREATED)

        except Course.DoesNotExist:
            return Response(
                {'Ошибка': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'Ошибка': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

