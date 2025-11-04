# GitHub Actions Workflow - Настройка секретов

Этот workflow автоматически собирает Docker образ и развертывает приложение на удаленном сервере.

## Необходимые секреты в GitHub

Для работы workflow необходимо настроить следующие секреты в настройках репозитория:
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

### Обязательные секреты:

1. **SSH_HOST** - IP адрес или доменное имя удаленного сервера
   - Пример: `192.168.1.100` или `myserver.example.com`

2. **SSH_USER** - Имя пользователя для SSH подключения
   - Пример: `deploy` или `root` или `ubuntu`

3. **SSH_PRIVATE_KEY** - Приватный SSH ключ для подключения к серверу
   - Содержимое файла `~/.ssh/id_rsa` (без публичного ключа)
   - Публичный ключ должен быть добавлен в `~/.ssh/authorized_keys` на сервере

### Автоматические секреты:

- **GITHUB_TOKEN** - Автоматически предоставляется GitHub, используется для push в GHCR

## Настройка SSH на сервере

1. Создайте SSH ключ (если еще нет):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions"
   ```

2. Скопируйте публичный ключ на сервер:
   ```bash
   ssh-copy-id user@your-server
   ```

3. Добавьте публичный ключ в `~/.ssh/authorized_keys` на сервере

4. Убедитесь, что на сервере установлен Docker:
   ```bash
   docker --version
   ```

## Настройка GitHub Container Registry

GHCR автоматически создается при первом push. Убедитесь, что пакеты не приватные или настройте права доступа.

Для доступа к приватным пакетам на сервере:
1. Создайте Personal Access Token с правами `read:packages`
2. Используйте его для логина: `docker login ghcr.io -u USERNAME -p TOKEN`

## Триггеры workflow

Workflow запускается:
- При push в ветки `main` или `master`
- Вручную через `Actions` → `Build and Deploy` → `Run workflow`

## Что делает workflow

### Job 1: build-and-push
- Проверяет код из репозитория
- Собирает Docker образ
- Пушит образ в GitHub Container Registry
- Использует кэш для ускорения сборки

### Job 2: deploy
- Выполняется только после успешной сборки
- Подключается к серверу по SSH
- Останавливает старый контейнер
- Скачивает новый образ из GHCR
- Запускает новый контейнер
- Показывает статус и логи

## Проверка деплоя

После успешного выполнения workflow проверьте:
```bash
# На сервере
docker ps
docker logs test-backend-api

# Проверка доступности API
curl http://your-server:8000/health
```
