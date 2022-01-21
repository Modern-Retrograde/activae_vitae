# Общая конфигурации проекта.

flask_debug = True
recreate_database = True  # Опасная переменная, от которой зависит целостность всей БД.

sqlalchemy_arguments = {
    "url": "sqlite:///activae_vitae.db"
}

token_len = 64
token_symbols = "qwertyuiopasdfghjklzxcvbnm_1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
token_expire_date = 86400
