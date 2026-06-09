#!/bin/bash
# Очистка логов и кэша
truncate -s 0 /var/log/*.log
apt-get clean

# Добавляем всё в гит
git add .
git commit -m "auto-deploy: $(date)"

# Пушим
git push origin feature/webview-ui

echo "---"
echo "Готово! Иди в GitHub Actions: https://github.com/$(git remote get-url origin | cut -d: -f2 | sed 's/.git//')/actions"
