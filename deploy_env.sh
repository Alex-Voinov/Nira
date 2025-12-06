#!/bin/bash

# ----------------------------
# Настройки
# ----------------------------
LOCAL_PROJECT_DIR="/c/Users/Voino/Documents/Nira"
REMOTE_USER="root"
REMOTE_HOST="62.113.44.39"
REMOTE_PROJECT_DIR="/var/www/nira"

# ----------------------------
# Перенос файлов из корня проекта
# ----------------------------
echo "Copying root .env files..."
scp "$LOCAL_PROJECT_DIR/.env" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/"
scp "$LOCAL_PROJECT_DIR/.env.prod" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/"
scp "$LOCAL_PROJECT_DIR/.env.dev" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/"

# ----------------------------
# Перенос файлов из папки app
# ----------------------------
echo "Copying app/.env files..."
scp "$LOCAL_PROJECT_DIR/app/.env" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/app/"
scp "$LOCAL_PROJECT_DIR/app/.env.production" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/app/"
scp "$LOCAL_PROJECT_DIR/app/.env.development" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/app/"

# ----------------------------
# Установка прав на сервере
# ----------------------------
echo "Setting permissions..."
ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
chmod 600 $REMOTE_PROJECT_DIR/.env*
chmod 600 $REMOTE_PROJECT_DIR/app/.env*
EOF

echo "✅ All .env files transferred and permissions set."
