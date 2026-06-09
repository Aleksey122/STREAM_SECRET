import sys, os
sys.path.append(os.getcwd())
from ui_controller import UIController

ctrl = UIController()
print(ctrl.handle_mic())
print(ctrl.handle_file())
