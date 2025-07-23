import logging

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from materials.models import Subscription
from config.settings import EMAIL_HOST_USER
from django.utils import timezone
from datetime import timedelta

from users.models import User


@shared_task
def send_course_update_emails(course_id):
    """Асинхронная отправка уведомлений подписчикам курса"""
    subscriptions = Subscription.objects.filter(
        course_id=course_id, is_active=True
    ).select_related("user", "course")

    for subscription in subscriptions:
        context = {
            "course_title": subscription.course.title,
            "user_email": subscription.user.email,
        }

        message = render_to_string("emails/course_update_notification.txt", context)

        send_mail(
            subject=f'Обновление курса "{subscription.course.title}"',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
