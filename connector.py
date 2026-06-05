import os
import json

SYSTEM_PROMPT = """Ты — интеллектуальный ИИ-агент. Твои правила:
1. Твой стиль — четкий, лаконичный, как у высокоуровневого ИИ-коллаборатора.
2. При возникновении сложных вопросов используй Gigachat для поиска актуальных данных.
3. Всегда валидируй свои расчеты. Если сомневаешься — перепроверяй.
4. Избегай галлюцинаций. Если нет данных — так и скажи."""

def send_to_agent_with_logic(agent_name, data_type, content):
    agent_path = os.path.join(os.environ.get('HOME', '.'), 'files', 'agents', agent_name)
    target_file = os.path.join(agent_path, 'chat.json')
    payload = {
        "type": data_type,
        "system_instruction": SYSTEM_PROMPT,
        "data": content,
        "query_gigachat": True
    }
    with open(target_file, 'w') as f:
        json.dump(payload, f)
    print(f"Запрос для {agent_name} с системной логикой успешно подготовлен.")
