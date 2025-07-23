import logging
from datetime import timezone

from dateutil.relativedelta import relativedelta

from config.celery import app
from users.models import User

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def deactivate_inactive_users() -> None:
    """Задача для деактивации пользователей, не заходивших более месяца"""
    inactive_threshold = timezone.now() - relativedelta(months=1)

    inactive_users = User.objects.filter(
        last_login__lt=inactive_threshold, is_active=True
    )

    count = inactive_users.update(is_active=False)

    logger.info(f"Deactivated {count} inactive users")
