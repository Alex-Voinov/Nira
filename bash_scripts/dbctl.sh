#!/bin/bash

# ----------------------------
# Настройки подключения к серверу
# ----------------------------
REMOTE_USER="root"
REMOTE_HOST="62.113.44.39"
DB_USER="postgres"
DB_NAME="NiraDB"

# ----------------------------
# Меню
# ----------------------------
options=(
"1. Написать SQL команду вручную"
"2. Показать текущие таблицы"
"3. Удалить таблицу с зависимостями"
"4. Удалить ВСЕ таблицы"
"5. Выход"
)

selected=0

draw_menu() {
    clear
    echo "Управление БД: $DB_NAME на $REMOTE_HOST"
    echo "Навигация: ↑ ↓ | Enter"
    echo "----------------------------"
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

    read -rsn1 key
    if [[ $key == $'\x1b' ]]; then
        read -rsn2 key
        if [[ $key == '[A' ]]; then
            ((selected--))
            (( selected < 0 )) && selected=$((${#options[@]} - 1))
        elif [[ $key == '[B' ]]; then
            ((selected++))
            (( selected >= ${#options[@]} )) && selected=0
        fi
    elif [[ $key == "" ]]; then
        break
    fi
done

clear

# ----------------------------
# Логика команд через SSH + sudo
# ----------------------------
case $selected in

0)
    echo "Интерактивный SQL-режим на сервере"
    echo "Для выхода введи: exit"
    echo "----------------------------"
    while true; do
        echo -n "sql> "
        read -r sql
        [[ "$sql" == "exit" ]] && break
        ssh "$REMOTE_USER@$REMOTE_HOST" "sudo -u $DB_USER psql -d $DB_NAME -c \"$sql\""
    done
    ;;

1)
    echo "Текущие таблицы:"
    ssh "$REMOTE_USER@$REMOTE_HOST" "sudo -u $DB_USER psql -d $DB_NAME -c '\dt'"
    ;;

2)
    echo "Введите имя таблицы:"
    read -r table
    echo "Удаление таблицы $table со всеми зависимостями..."
    ssh "$REMOTE_USER@$REMOTE_HOST" "sudo -u $DB_USER psql -d $DB_NAME -c 'DROP TABLE IF EXISTS $table CASCADE;'"
    ;;

3)
    echo "⚠️ ВНИМАНИЕ: Будут удалены ВСЕ таблицы!"
    read -p "Введите YES для подтверждения: " confirm
    if [[ "$confirm" == "YES" ]]; then
        echo "Удаление всех таблиц..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "sudo -u $DB_USER psql -d $DB_NAME -c \"DO \$\$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE'; END LOOP; END \$\$;\""
    else
        echo "Отменено."
    fi
    ;;

4)
    exit 0
    ;;
esac
