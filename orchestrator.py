from inspector_base import InspectorBase

def main():
    # Инициализация с твоими зашифрованными данными
    inspector = InspectorBase(credentials="ENCRYPTED_DATA_PATH")
    
    print("--- Digital Inspector Active ---")
    print(inspector.get_status())
    
    # Здесь позже добавим логику запуска проверок по расписанию
    # inspector.safe_check()

if __name__ == "__main__":
    main()
