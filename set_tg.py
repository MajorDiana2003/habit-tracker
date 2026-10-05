import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from habits_app.tasks import send_habit_reminders

print("Запуск симуляции отправки напоминаний...")
send_habit_reminders()
print("Готово! Проверь, появился ли файл 'telegram_history.log' в корне твоего проекта.")







