from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from habits_app.models import Habit
from habits_app.serializers import HabitSerializer
from habits_app.paginators import HabitPagination
from habits_app.permissions import IsOwner
from django.http import HttpResponse


class HabitViewSet(ModelViewSet):
    """
    CRUD для привычек текущего пользователя.
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Если юзер не авторизован (например, при генерации схемы документации)
        if not self.request.user.is_authenticated:
            return Habit.objects.none()

        # Для метода LIST возвращаем только свои привычки
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user).order_by('id')


        return Habit.objects.all().order_by('id')

    def perform_create(self, serializer):
        # Автоматически привязываем создаваемую привычку к текущему пользователю
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    """
    Список всех публичных привычек (доступен всем авторизованным пользователям только для чтения).
    """
    queryset = Habit.objects.filter(is_public=True).order_by('id')
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]


def home_page_view(request):
    """
    Контроллер для отображения главной страницы с полезными ссылками и статусом Telegram.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Трекер привычек API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; color: #333; }
            h1 { color: #2c3e50; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 15px 0; background: #fff; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            a { text-decoration: none; color: #3498db; font-weight: bold; font-size: 18px; }
            a:hover { color: #2980b9; }
            span { color: #7f8c8d; font-size: 14px; display: block; margin-top: 5px; }

            /* Стили для блока уведомления о Telegram */
            .status-banner { 
                background-color: #fff3cd; 
                border-left: 6px solid #ffc107; 
                color: #856404; 
                padding: 20px; 
                border-radius: 5px; 
                margin-bottom: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .status-banner h3 { margin-top: 0; color: #856404; }
            .status-badge {
                display: inline-block;
                background-color: #17a2b8;
                color: white;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать в API Трекера привычек! 🚀</h1>

        <!-- Блок статуса интеграции с Telegram -->
        <div class="status-banner">
            <h3>📢 Внимание: Режим демонстрации и логирования</h3>
            <p>В связи с сетевыми ограничениями доступа к официальному <strong>api.telegram.org</strong> на стороне провайдера, бэкенд автоматически переключен в режим <strong>Mock-тестирования (Симуляции)</strong>.</p>
            <p>Все периодические задачи Celery Beat успешно генерируют уведомления и записывают их в локальный файл автономной истории: <code>telegram_history.log</code> в корне проекта.</p>
            <div class="status-badge">Celery + Redis: ACTIVE</div>
            <div class="status-badge" style="background-color: #6c757d;">Telegram API: MOCKED (LOG MODE)</div>
        </div>

        <p>Ниже представлены быстрые ссылки для навигации по курсовой работе:</p>
        <ul>
            <li>
                <a href="/api/docs/swagger/" target="_blank">📖 Документация Swagger UI</a>
                <span>Интерактивная карта эндпоинтов, где можно протестировать запросы.</span>
            </li>
            <li>
                <a href="/api/docs/redoc/" target="_blank">📄 Документация ReDoc</a>
                <span>Альтернативный строгий вариант отображения спецификации API.</span>
            </li>
            <li>
                <a href="/admin/" target="_blank">👑 Административная панель Django</a>
                <span>Вход в панель управления базой данных (требуется создать суперпользователя).</span>
            </li>
            <li>
                <a href="/api/habits/public/" target="_blank">🌐 Список публичных привычек</a>
                <span>Эндпоинт для просмотра привычек, которые пользователи сделали публичными.</span>
            </li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html_content)
