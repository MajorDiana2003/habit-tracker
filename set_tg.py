import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings


def test_live_send():
    # Пропишите сюда ваш точный цифровой ID
    my_chat_id = 1886262561
    token = settings.TELEGRAM_BOT_TOKEN
    print(f"Используется токен бота: {token[:15]}...")
    print(f"Отправка тестового уведомления на Chat ID: {my_chat_id}...")

    url = (
        "https://api.telegram.org/bot"
        f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )
    text = "🔥 Ура! Проверка связи прошла успешно! Код бэкенда курсовой работает идеально на 100%!"

    try:
        response = requests.post(url, json={"chat_id": my_chat_id, "text": text}, timeout=10)
        if response.status_code == 200:
            print("\n==================================================")
            print("🔥 ОТЛИЧНО! Telegram API подтвердил доставку!")
            print("Проверьте телефон, сообщение уже у вас!")
            print("==================================================")
        else:
            print(f"\n❌ Ошибка Telegram API: Status {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"\n❌ Ошибка сети при запросе к Telegram: {e}")


if __name__ == "__main__":
    test_live_send()
