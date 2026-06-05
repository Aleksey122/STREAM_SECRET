import os
import requests
import subprocess

def check_and_update():
    # Проверка наличия интернета и обновлений
    try:
        remote_ver = requests.get("https://raw.githubusercontent.com/ВАШ_НИК/РЕПОЗИТОРИЙ/main/version.txt").text.strip()
        current_ver = "1.0"
        if remote_ver != current_ver:
            print("Найдено обновление, качаю...")
            # Сюда можно добавить логику скачивания
    except Exception as e:
        print(f"Ошибка проверки: {e}")

if __name__ == "__main__":
    check_and_update()
