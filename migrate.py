import shutil
import os

PERSISTENT_DIR = os.path.join(os.environ.get('HOME', '.'), 'files', 'agents')

def setup_agents():
    if not os.path.exists(PERSISTENT_DIR):
        os.makedirs(PERSISTENT_DIR)
        if os.path.exists('/root/gemini_bot'):
            shutil.copytree('/root/gemini_bot', os.path.join(PERSISTENT_DIR, 'gemini_bot'))
        if os.path.exists('/root/zolotoy_arhiv'):
            shutil.copytree('/root/zolotoy_arhiv', os.path.join(PERSISTENT_DIR, 'zolotoy_arhiv'))
        print("Агенты успешно переехали в зону вечного хранения")
    else:
        print("Агенты уже находятся в зоне хранения")

if __name__ == "__main__":
    setup_agents()
