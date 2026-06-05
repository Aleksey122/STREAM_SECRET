from bridge import route_to_bot, dispatch_task

def process_user_input(user_input):
    # Определяем, какому боту отдать задачу
    task = route_to_bot(user_input)
    # Отправляем задачу в нужный JSON-файл
    dispatch_task(user_input, task)
    print(f"Задача '{task}' успешно направлена в очередь.")

# Пример вызова для проверки
if __name__ == "__main__":
    test_msg = "Привет, это тестовая система"
    process_user_input(test_msg)
