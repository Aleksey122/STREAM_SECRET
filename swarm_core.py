import json
import time
import requests
import os

def agent_loop(agent_name):
    print(f"Агент {agent_name} активирован...")
    chat_file = 'shared_chat.json'
    
    while True:
        try:
            if os.path.exists(chat_file):
                with open(chat_file, 'r') as f:
                    data = json.load(f)
                
                if data.get('task'):
                    print(f"Агент {agent_name} взял задачу: {data['task']}")
                    # Логика запроса к Gigachat будет здесь
                    with open(chat_file, 'w') as f:
                        json.dump({"task": None, "status": "processed"}, f)
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(2)

if __name__ == "__main__":
    agent_loop("University_Agent_01")
