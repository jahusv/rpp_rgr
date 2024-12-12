#!/bin/bash

DB_HOST="127.0.0.1"
DB_NAME="rgr"
DB_USER="sajfulina_alina"


# Функция для настройки базы данных PostgreSQL
setup_database() {
    # Создание базы данных, если она не существует
    PGPASSWORD=$DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

    # Создание таблиц
    PGPASSWORD=$DB_HOST -U $DB_USER -d $DB_NAME -c "
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        cost FLOAT NOT NULL,
        frequency INT NOT NULL,
        start_date DATE NOT NULL
    );
    "
    echo "Готово"
}

# Функция для установки зависимостей Python
install_dependencies() {
    # Создание виртуального окружения
    python3 -m venv venv

    # Активируем виртуальное окружение
    source venv/bin/activate

    # Установка зависимостей из requirements.txt
    pip install -r requirements.txt

    echo "Готово"
}

# Функция для запуска Flask-приложения
start_app() {
     # Активируем виртуальное окружение
    source venv/bin/activate

    # Запуск приложения
    export FLASK_APP=app.py
    flask run

    echo "Готово"
}

# Функция для остановки Flask-приложения
stop_app() {
    # Поиск процесса Flask и его завершение
    pkill -f "flask run"

    echo "Готово"
}

# Главная логика, которая выполняет нужную функцию в зависимости от аргумента
case "$1" in
    setup_database)
        setup_database
        ;;
    install_dependencies)
        install_dependencies
        ;;
    start_app)
        start_app
        ;;
    stop_app)
        stop_app
        ;;
    *)
        echo "Неверная команда"
        exit 1
        ;;
esac
