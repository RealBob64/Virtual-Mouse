from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import cv2
from MouseWidget import MouseWidget


class MouseGUI(QWidget):
    def __init__(self, worker):
        super().__init__()

        self.worker = worker

        self.setWindowTitle("Virtual Mouse")

        # --- UI Elements ---
        self.video_label = QLabel()
        self.gesture_label = QLabel("Gesture: None")

        #self.mouse3d = MouseWidget()
        #self.mouse3d.setMinimumSize(300, 300)

        # Controls
        self.toggle_button = QPushButton("Pause")
        self.toggle_button.clicked.connect(self.toggle_worker)

        self.calibrate_button = QPushButton("Calibrate")
        self.calibrate_button.clicked.connect(self.calibrate)

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(10)
        self.sensitivity_slider.setValue(5)
        self.sensitivity_slider.valueChanged.connect(self.update_sensitivity)

        # --- Layouts ---
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.video_label)
        #top_layout.addWidget(self.mouse3d)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.toggle_button)
        controls_layout.addWidget(self.calibrate_button)
        controls_layout.addWidget(self.sensitivity_slider)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.gesture_label)
        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

        # --- Connections ---
        self.worker.frame_ready.connect(self.update_frame)
        self.worker.gesture_ready.connect(self.update_gesture)

        self.running = True

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape

        image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        self.video_label.setPixmap(pixmap)

    def update_gesture(self, gesture):
        self.gesture_label.setText(f"Gesture: {gesture}")

        # update 3D mouse
        #self.mouse3d.update_state(gesture)

    # --- Controls ---
    def toggle_worker(self):
        if self.running:
            self.worker.running = False
            self.toggle_button.setText("Resume")
        else:
            self.worker.running = True
            if not self.worker.isRunning():
                self.worker.start()
            self.toggle_button.setText("Pause")

        self.running = not self.running

    def calibrate(self):
        print("Calibration triggered (implement later)")

    def update_sensitivity(self, value):
        print(f"Sensitivity: {value}")
        # hook into controller later

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()
        event.accept()