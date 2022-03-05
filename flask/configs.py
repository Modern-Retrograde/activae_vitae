# Общая конфигурации проекта.
from random import choice as random_choice

flask_debug = True
flask_csrf_enabled = True

recreate_database = False  # Опасная переменная, от которой зависит целостность всей БД.

sqlalchemy_arguments = {
    "url": "sqlite:///activae_vitae.db"
}

token_len = 64
token_symbols = "qwertyuiopasdfghjklzxcvbnm_1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
token_expire_date = 86400
flask_secret_key = "".join([random_choice(token_symbols) for _ in range(token_len)])
date_format = "%d.%m.%Y %H:%M"

# Права доступа для зарегистрированных аккаунтов.
all_roles_in_projects = {
    # Директор.
    # Директор всегда прав...
    "director": {
        "verify_accounts": True,  # Подтверждать сторонние аккаунты.
        "create_events": True,  # Создавать события.
        "edit_events": True,  # Редактировать события.
        "delete_events": True,  # Удалять любые события.
        "delete_own_events": True,  # Удалять свои мероприятия.
        "edit_account_roles": True,  # Изменение роли любому аккаунту.
        "edit_own_account": True,  # Редактирование своего же аккаунта.
        "get_event_stats": True,  # Получение статистики о мероприятии.
    },
    # Учитель-организатор.
    "teacher": {
        "verify_accounts": False,
        "create_events": True,
        "edit_events": True,
        "delete_events": False,
        "delete_own_events": True,
        "edit_account_roles": False,
        "edit_own_account": True,
        "get_event_stats": False,
    },
    # Ученик.
    "student": {
        "verify_accounts": False,
        "create_events": False,
        "edit_events": False,
        "delete_events": False,
        "delete_own_events": False,
        "edit_account_roles": False,
        "edit_own_account": True,
        "get_event_stats": False,
    },
    # Я тестер, мне всё можно.
    "tester": {
        "verify_accounts": True,  # Подтверждать сторонние аккаунты.
        "create_events": True,  # Создавать события.
        "edit_events": True,  # Редактировать события.
        "delete_events": True,  # Удалять любые события.
        "delete_own_events": True,  # Удалять свои мероприятия.
        "edit_account_roles": True,  # Изменение роли любому аккаунту.
        "edit_own_account": True,  # Редактирование своего же аккаунта.
        "get_event_stats": True,  # Получение статистики о мероприятии.
    }
}
