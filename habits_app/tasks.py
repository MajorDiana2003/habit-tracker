import os
from datetime import datetime
from celery import shared_task
from habits_app.models import Habit


@shared_task
def send_habit_reminders():
    """
    Периодическая задача для рассылки напоминаний о привычках.
    Вместо нестабильной отправки в сеть записывает уведомления в локальный файл-лог.
    """
    now = datetime.now().time()


    # строгий минутный фильтр
    habits = Habit.objects.select_related('user').filter(
        time__hour=now.hour,
        time__minute=now.minute
    )

    log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'telegram_history.log')

    for habit in habits:
        if habit.user.telegram_chat_id:
            # Формируем красивый текст сообщения для лога
            message = (
                f"========================================\n"
                f"🤖 [DIANA_HABIT_BOT] СИМУЛЯЦИЯ ОТПРАВКИ В TELEGRAM\n"
                f"📅 Время отправки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"👤 Получатель (Chat ID): {habit.user.telegram_chat_id} ({habit.user.email})\n"
                f"----------------------------------------\n"
                f"⏰ Напоминание! Пора выполнить привычку:\n"
                f"📌 Действие: {habit.action}\n"
                f"📍 Место: {habit.place}\n"
            )

            if hasattr(habit, 'reward') and habit.reward:
                message += f"🎁 Награда после выполнения: {habit.reward}\n"
            elif hasattr(habit, 'associated_habit') and habit.associated_habit:
                message += f"🎉 Связанная приятная привычка: {habit.associated_habit.action}\n"

            message += "========================================\n\n"

            # Записываем сформированное уведомление в файл telegram_history.log
            try:
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(message)
                print(f"✅ Имитация отправки для {habit.user.email} успешно зафиксирована в telegram_history.log")
            except Exception as e:
                print(f"Ошибка записи лога: {e}")



