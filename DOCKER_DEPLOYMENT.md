# Docker Deployment Guide

## Архитектура

```
┌─────────────────────┐
│  Telegram Users     │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐      HTTP API       ┌─────────────────────┐
│  freebot-telegram   │ ─────────────────> │ freebotsigur-backend│
│  (Python Bot)       │  Authorization:     │  (Java REST API)    │
│  Port: -            │  phone_number       │  Port: 8080         │
└──────────┬──────────┘                     └──────────┬──────────┘
           │                                           │
           │                                           │
           v                                           v
    ┌──────────┐                            ┌─────────────────┐
    │ MongoDB  │                            │  PostgreSQL     │
    │ Port:    │                            │  Port: 5432     │
    │ 27017    │                            │                 │
    └──────────┘                            └─────────────────┘
                                                      │
                                                      v
                                            ┌─────────────────┐
                                            │     Redis       │
                                            │  Port: 6379     │
                                            └─────────────────┘
```

## Компоненты

### 1. freebotsigur-backend (Java Spring Boot)
- REST API backend
- Порт: 8080
- БД: PostgreSQL
- Кеш: Redis
- Интеграции: Sigur, AST, SMTP

### 2. freebot-telegram (Python)
- Telegram bot клиент
- Вызывает freebotsigur-backend API
- БД: MongoDB (состояние пользователя)

### 3. Databases
- **MongoDB**: состояние бота, кеш проектов
- **PostgreSQL**: основная БД backend
- **Redis**: кеширование backend

## Установка

### Шаг 1: Подготовка репозиториев

```bash
# Структура директорий
Desktop/
├── freebotsigur/                              # Java backend
│   ├── Dockerfile                             # создать
│   ├── src/
│   └── pom.xml
└── chat-bot-python-service-release-rubius/    # Python bot
    ├── docker-compose.unified.yml             # главный compose
    ├── .env                                    # конфигурация
    └── Dockerfile                              # уже есть
```

**Клонировать Java backend:**
```bash
cd Desktop
git clone https://github.com/gracee02a57b8-cloud/freebotsigur.git
```

**Создать Dockerfile в freebotsigur/:**
```bash
cd freebotsigur
# Скопировать содержимое из Dockerfile.backend
# (файл создан в репозитории Python бота)
cp ../chat-bot-python-service-release-rubius/Dockerfile.backend ./Dockerfile
```

### Шаг 2: Конфигурация

**Создать .env файл:**
```bash
cd chat-bot-python-service-release-rubius
cp .env.example .env
nano .env  # или используйте любой редактор
```

**Обязательные переменные:**
```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz  # получить от @BotFather
MONGO_PASSWORD=your_secure_password_here
```

**Опциональные переменные:**
- SMTP_* - для email уведомлений
- SIGUR_* - интеграция с системой Sigur
- AST_* - интеграция с системой AST

### Шаг 3: Запуск

**Запуск всей системы:**
```bash
cd chat-bot-python-service-release-rubius
docker-compose -f docker-compose.unified.yml up --build
```

**Запуск в фоновом режиме:**
```bash
docker-compose -f docker-compose.unified.yml up -d --build
```

**Просмотр логов:**
```bash
# Все сервисы
docker-compose -f docker-compose.unified.yml logs -f

# Только бот
docker-compose -f docker-compose.unified.yml logs -f freebot-telegram

# Только backend
docker-compose -f docker-compose.unified.yml logs -f freebotsigur-backend
```

**Остановка:**
```bash
docker-compose -f docker-compose.unified.yml down
```

**Полная очистка (с удалением данных):**
```bash
docker-compose -f docker-compose.unified.yml down -v
```

## Проверка работоспособности

### 1. Healthcheck endpoints

**Java Backend:**
```bash
curl http://localhost:8080/api/healthcheck
```

Ожидаемый ответ:
```json
{
  "databaseOk": true,
  "integrationDatabaseOk": true,
  "redisOk": true,
  "sigurOk": false,
  "astOk": false,
  "smtpOk": false
}
```

**PostgreSQL:**
```bash
docker exec -it freebot-postgres psql -U postgres -d freebotsigur -c "SELECT version();"
```

**MongoDB:**
```bash
docker exec -it freebot-mongodb mongosh -u admin -p password --eval "db.adminCommand('ping')"
```

**Redis:**
```bash
docker exec -it freebot-redis redis-cli ping
```

### 2. Проверка Telegram бота

1. Найдите бота в Telegram по username
2. Отправьте команду `/start`
3. Нажмите "Поделиться контактом"
4. Проверьте, что бот ответил

### 3. Проверка логов

```bash
# Должны быть сообщения о подключении к БД
docker-compose -f docker-compose.unified.yml logs freebotsigur-backend | grep "Started"

# Должны быть сообщения от Telegram API
docker-compose -f docker-compose.unified.yml logs freebot-telegram | grep "Telegram"
```

## Troubleshooting

### Проблема: Backend не может подключиться к PostgreSQL

**Симптомы:**
```
Connection refused: postgres:5432
```

**Решение:**
```bash
# Проверить, что PostgreSQL запущен
docker-compose -f docker-compose.unified.yml ps postgres

# Проверить логи PostgreSQL
docker-compose -f docker-compose.unified.yml logs postgres

# Перезапустить только PostgreSQL
docker-compose -f docker-compose.unified.yml restart postgres
```

### Проблема: Бот не видит backend

**Симптомы:**
```
ConnectionError: http://freebotsigur-backend:8080
```

**Решение:**
```bash
# Проверить, что backend запущен
docker-compose -f docker-compose.unified.yml ps freebotsigur-backend

# Проверить сеть
docker network inspect freebot-network

# Проверить, что backend отвечает
docker exec -it freebot-telegram curl http://freebotsigur-backend:8080/api/healthcheck
```

### Проблема: "Permission denied (publickey)"

**Решение:**
```bash
# Убедитесь, что используется HTTPS URL для Git
cd freebotsigur
git remote -v
git remote set-url origin https://github.com/gracee02a57b8-cloud/freebotsigur.git
```

### Проблема: Недостаточно памяти

**Решение:**
```bash
# Увеличить лимиты Docker Desktop
# Settings → Resources → Memory → 4GB+

# Или ограничить Java heap
# В docker-compose.unified.yml:
environment:
  JAVA_OPTS: "-Xmx256m -Xms128m"
```

## Production Deployment

### Использование docker-compose.prod.yml (опционально)

Создайте `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  freebotsigur-backend:
    environment:
      DATABASE_URL: ${PROD_DATABASE_URL}
      REDIS_HOST: ${PROD_REDIS_HOST}
    restart: always

  freebot-telegram:
    restart: always

  postgres:
    volumes:
      - /data/postgres:/var/lib/postgresql/data

  mongodb:
    volumes:
      - /data/mongo:/data/db
```

**Запуск:**
```bash
docker-compose -f docker-compose.unified.yml -f docker-compose.prod.yml up -d
```

### CI/CD Integration

**GitLab CI:**
```yaml
deploy:
  script:
    - docker-compose -f docker-compose.unified.yml pull
    - docker-compose -f docker-compose.unified.yml up -d
```

**Azure Pipelines:**
```yaml
- task: DockerCompose@0
  inputs:
    dockerComposeFile: 'docker-compose.unified.yml'
    action: 'Run services'
```

## Maintenance

### Backup данных

**PostgreSQL:**
```bash
docker exec freebot-postgres pg_dump -U postgres freebotsigur > backup_postgres_$(date +%Y%m%d).sql
```

**MongoDB:**
```bash
docker exec freebot-mongodb mongodump --username admin --password password --out /tmp/backup
docker cp freebot-mongodb:/tmp/backup ./backup_mongo_$(date +%Y%m%d)
```

### Update сервисов

```bash
# Pull новых образов
docker-compose -f docker-compose.unified.yml pull

# Пересобрать и перезапустить
docker-compose -f docker-compose.unified.yml up -d --build

# Или для конкретного сервиса
docker-compose -f docker-compose.unified.yml up -d --build freebot-telegram
```

### Мониторинг

```bash
# Статус контейнеров
docker-compose -f docker-compose.unified.yml ps

# Использование ресурсов
docker stats

# Логи в реальном времени
docker-compose -f docker-compose.unified.yml logs -f --tail=100
```

## Ссылки

- [Service freebot GitHub](https://github.com/gracee02a57b8-cloud/Freebot-service)
- [freebotsigur GitHub](https://github.com/gracee02a57b8-cloud/freebotsigur)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
