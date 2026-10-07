import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits_app.models import Habit


def send_telegram_message(chat_id: str, text: str) -> None:
    """Прямая отправка текстового сообщения в Telegram-чат."""
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN")

    url = (
        "https://api.telegram.org/bot"
        f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        json={"chat_id": chat_id, "text": text},
        timeout=10
    )
    response.raise_for_status()


@shared_task(
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    max_retries=5,
)
def send_habit_reminders() -> None:
    """Периодическая задача Celery для проверки и отправки напоминаний."""
    now = timezone.localtime()

    # Фильтруем привычки по текущему часу и минуте, у которых у пользователя заполнен chat_id
    habits = Habit.objects.select_related("user").filter(
        time__hour=now.hour,
        time__minute=now.minute,
        user__telegram_chat_id__isnull=False,
    )

    for habit in habits:
        text = (
            f"Пора выполнить привычку: {habit.action}. "
            f"Место: {habit.place}."
        )
        send_telegram_message(habit.user.telegram_chat_id, text)
