from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None  # убираем username, используем email
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту!"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона!",
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f"{self.user.email} - {self.payment_date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'