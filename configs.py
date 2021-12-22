# Общая конфигурации проекта.

flask_debug = True
recreate_database = True  # Опасная переменная, от которой зависит целостность всей БД.

sqlalchemy_arguments = {
    "url": "sqlite:///activae_vitae.db"
}
