# shiki-recs

## Документация Shikimori API

[Документация](https://shikimori.me/api/doc)

Доступ к странице может не работать без VPN.
Полезно смотреть не только на v2, но и на v1. 

## Работа с базой данных

Создание новой миграции: 
```bash
alembic revision --autogenerate -m 'migration_name'
```

Создание выполнение всех миграций: 
```bash
alembic upgrade head
```

Откатывание до пустой базы данных: 
```bash
alembic downgrade base
```
