#!/bin/bash

# ----------------------------
# Настройки
# ----------------------------
LOCAL_PROJECT_DIR="/c/Users/Voino/Documents/Nira"
REMOTE_USER="root"
REMOTE_HOST="62.113.44.39"
REMOTE_PROJECT_DIR="/var/www/nira"

# ----------------------------
# Меню выбора
# ----------------------------
options=("env" "dist" "весь проект" "выход")
selected=0  # по умолчанию пункт "env"

draw_menu() {
    clear
    echo "Выберите, что деплоить (стрелки ↑/↓, Enter для выбора):"
    for i in "${!options[@]}"; do
        if [ $i -eq $selected ]; then
            echo -e "  (\e[1;32m•\e[0m) ${options[$i]}"
        else
            echo "  ( ) ${options[$i]}"
        fi
    done
}

while true; do
    draw_menu

    # Чтение одной клавиши без Enter
    read -rsn1 key
    if [[ $key == $'\x1b' ]]; then
        read -rsn2 key
        if [[ $key == '[A' ]]; then
            ((selected--))
            if [ $selected -lt 0 ]; then selected=$((${#options[@]}-1)); fi
        elif [[ $key == '[B' ]]; then
            ((selected++))
            if [ $selected -ge ${#options[@]} ]; then selected=0; fi
        fi
    elif [[ $key == "" ]]; then
        break
    fi
done

CHOICE=${options[$selected]}
echo "Вы выбрали: $CHOICE"

# ----------------------------
# Функция для перезапуска служб и проверки статуса
# ----------------------------
restart_services() {
    echo "🔄 Перезапускаем службы nira_api и nira_bot..."
    ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
sudo systemctl restart nira_api
sudo systemctl restart nira_bot

echo
echo "📊 Статус служб после перезапуска:"
sudo systemctl status nira_api --no-pager
sudo systemctl status nira_bot --no-pager
EOF
}

# ----------------------------
# Функция прогресс-бара для папок
# ----------------------------
progress_bar() {
    local src=$1
    local dest=$2
    rsync -ah --progress "$src" "$dest"
}

# ----------------------------
# Деплой
# ----------------------------
case $CHOICE in
    "env")
        echo "🚀 Копируем только .env.prod и app/.env.production..."
        scp "$LOCAL_PROJECT_DIR/.env.prod" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/"
        scp "$LOCAL_PROJECT_DIR/app/.env.production" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/app/"

        ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
chmod 600 $REMOTE_PROJECT_DIR/.env.prod
chmod 600 $REMOTE_PROJECT_DIR/app/.env.production
EOF

        # Перезапуск служб
        restart_services
        ;;
    "dist")
        echo "🚀 Копируем папку app/dist..."
        progress_bar "$LOCAL_PROJECT_DIR/app/dist" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/app/"
        ;;
    "весь проект")
        echo "🚀 Копируем весь проект..."
        progress_bar "$LOCAL_PROJECT_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PROJECT_DIR/"

        ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
chmod 600 $REMOTE_PROJECT_DIR/.env*
chmod 600 $REMOTE_PROJECT_DIR/app/.env*
EOF

        # Перезапуск служб
        restart_services
        ;;
    "выход")
        exit 0
        ;;
esac

echo "✅ Деплой завершен!"
