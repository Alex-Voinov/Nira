#!/bin/bash

# ----------------------------
# Настройки
# ----------------------------
REMOTE_USER="root"
REMOTE_HOST="62.113.44.39"

# ----------------------------
# Список служб
# ----------------------------
services=("nira_api" "nira_bot" "выход")
selected=0  # по умолчанию первый пункт

draw_menu() {
    clear
    echo "Выберите службу для просмотра логов (стрелки ↑/↓, Enter для выбора):"
    for i in "${!services[@]}"; do
        if [ $i -eq $selected ]; then
            echo -e "  (\e[1;32m•\e[0m) ${services[$i]}"
        else
            echo "  ( ) ${services[$i]}"
        fi
    done
}

# ----------------------------
# Меню выбора службы
# ----------------------------
while true; do
    draw_menu

    # Чтение одной клавиши без Enter
    read -rsn1 key
    if [[ $key == $'\x1b' ]]; then
        read -rsn2 key
        if [[ $key == '[A' ]]; then
            ((selected--))
            if [ $selected -lt 0 ]; then selected=$((${#services[@]}-1)); fi
        elif [[ $key == '[B' ]]; then
            ((selected++))
            if [ $selected -ge ${#services[@]} ]; then selected=0; fi
        fi
    elif [[ $key == "" ]]; then
        break
    fi
done

CHOICE=${services[$selected]}
echo "Вы выбрали: $CHOICE"

# ----------------------------
# Просмотр логов
# ----------------------------
if [[ "$CHOICE" == "выход" ]]; then
    exit 0
else
    echo "🔄 Трансляция логов службы $CHOICE. Нажмите Ctrl+C для выхода."
    ssh "$REMOTE_USER@$REMOTE_HOST" "sudo journalctl -u $CHOICE -f --no-pager"
fi
