import json
import time
import os

def agent_loop():
    chat_file = 'shared_chat.json'
    print("Рой активирован...")
    while True:
        if os.path.exists(chat_file):
            try:
                with open(chat_file, 'r') as f:
                    data = json.load(f)
                if data.get('task'):
                    print(f"Обработка задачи: {data['task']}")
                    # Логика обработки...
                    with open(chat_file, 'w') as f:
                        json.dump({"task": None, "status": "done"}, f)
            except Exception as e:
                print(f"Ошибка: {e}")
        time.sleep(2)

if __name__ == "__main__":
    agent_loop()
