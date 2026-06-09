class UIController:
    def __init__(self):
        self.mic_active = False

    def handle_mic(self):
        self.mic_active = not self.mic_active
        return f"Mic state: {'ON' if self.mic_active else 'OFF'}"

    def handle_file(self):
        return "File system access: OK"
