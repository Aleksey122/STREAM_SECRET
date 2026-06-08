import uuid, time, os, requests, json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

KEY_FILE = "/root/my_project/.key"
AUTH_KEY = open(KEY_FILE).read().strip() if os.path.exists(KEY_FILE) else ""
HISTORY_FILE = "/root/my_project/history.json"
TOKEN_CACHE = {'token': None, 'expires': 0}

def get_token():
    if TOKEN_CACHE['token'] and time.time() < TOKEN_CACHE['expires']:
        return TOKEN_CACHE['token']
    try:
        r = requests.post(
            'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            headers={'RqUID': str(uuid.uuid4()), 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {AUTH_KEY}'},
            data={'scope': 'GIGACHAT_API_PERS'},
            verify=False, timeout=10)
        token = r.json().get('access_token')
        TOKEN_CACHE['token'] = token
        TOKEN_CACHE['expires'] = time.time() + 1500
        return token
    except:
        return None

def load_history():
    if os.path.exists(HISTORY_FILE):
        return json.load(open(HISTORY_FILE))
    return []

def save_history(history):
    json.dump(history[-100:], open(HISTORY_FILE, "w"), ensure_ascii=False)

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    token = get_token()
    if not token:
        return {"reply": "Ошибка авторизации GigaChat"}
    history = load_history()
    messages = [{"role": "system", "content": "Ты MAX AI - умный помощник."}]
    for h in history[-10:]:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["reply"]})
    messages.append({"role": "user", "content": msg.text})
    try:
        r = requests.post(
            'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            json={"model": "GigaChat", "messages": messages},
            verify=False, timeout=30)
        reply = r.json()['choices'][0]['message']['content']
        history.append({"user": msg.text, "reply": reply})
        save_history(history)
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Ошибка: {e}"}

@app.get("/health")
def health():
    return {"status": "ok", "key_loaded": bool(AUTH_KEY)}

@app.get("/history")
def get_history():
    return load_history()

@app.delete("/history")
def clear_history():
    save_history([])
    return {"status": "cleared"}
