import logging
from datetime import timezone, timedelta

from celery import shared_task

from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def deactivate_inactive_users():
    """Задача для деактивации пользователей, не заходивших более месяца"""
    inactive_threshold = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=inactive_threshold,
        is_active=True
    )

    count = inactive_users.update(is_active=False)

    logger.info(f"Deactivated {count} inactive users")
    return f"Deactivated {count} inactive users"