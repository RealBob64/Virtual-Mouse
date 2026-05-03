import sys
from PySide6.QtWidgets import QApplication
from MouseWorker import MouseWorker
from MouseGUI import MouseGUI

app = QApplication(sys.argv)

worker = MouseWorker()
window = MouseGUI(worker)

window.resize(800, 600)
window.show()

worker.start()

sys.exit(app.exec())