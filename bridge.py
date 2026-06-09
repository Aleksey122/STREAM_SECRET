import json
import os

def route_to_bot(user_msg):
    if "система" in user_msg or "команда" in user_msg:
        return "GEMINI_TASK"
    else:
        return "GOLD_TASK"

def dispatch_task(user_msg, task_type):
    if task_type == "GEMINI_TASK":
        target_file = "/root/gemini_bot/chat.json"
    else:
        target_file = "/root/zolotoy_arhiv/chat.json"
    
    with open(target_file, 'w') as f:
        json.dump([{"message": user_msg, "author": "Я"}], f)
