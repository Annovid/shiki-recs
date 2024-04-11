# shiki-recs

## Shikimori API

### Документация

[Документация](https://shikimori.me/api/doc)

Доступ к странице может не работать без VPN.
Полезно смотреть не только на v2, но и на v1.

### Принцип работы API

API делает запросы на 'https://shikimori.one/api' по следующиму принципу:
Создаётся инстанс класса `shikimori_api.ApiMethod`.
Обращение к дочерним методам конвертируется в путь url.
Последний метод должен быть одним из методов REST API (`GET`, `POST`, ...)
Параметры при вызове данного метода конвертируются в параметры запроса.

Ниже приведён пример подобного запроса.

**From Python**
```python
import shikimori_api

shikimori = shikimori_api.Shikimori()
shikimori_api = shikimori.get_api()
result = shikimori_api.user_rates.GET(user_id=1)
print(result)
```

**To Bash**

```shell
curl 'https://shikimori.one/api/user_rates?user_id=1'
```

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
