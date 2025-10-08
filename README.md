## Запуск проекта ##

1) Создать базу данных PostgresSQL, создать таблицы в базе (можно использовать src/reset_db.py)
2) Настроить переменные в следующих файлах:
    - .env
    - src/config.py
    - src/application/deployment/config.py
3) Запуск кода

```bash
python3.11 -m src.controllers.tg_bot
```

