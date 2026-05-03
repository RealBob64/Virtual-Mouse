from PySide6.QtCore import QThread, Signal
import mediapipe as mp
import MouseController
import MouseRecognizer
import cv2

class MouseWorker(QThread):
    frame_ready = Signal(object)
    gesture_ready = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True

        self.vc = cv2.VideoCapture(0)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.controller = MouseController.Controller()
        self.recognizer = MouseRecognizer.Recognizer()

    def run(self):
        with self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5
        ) as hands:

            while self.running and self.vc.isOpened():
                read_success, frame = self.vc.read()
                if not read_success:
                    break

                frame = cv2.flip(frame, 1)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = hands.process(image_rgb)

                gesture = "None"

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

                        gesture = self.recognizer.get_gesture(landmarks)
                        self.controller.handle(gesture, landmarks)

                        self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS
                        )

                # send data to UI
                self.frame_ready.emit(frame)
                self.gesture_ready.emit(gesture)

    def stop(self):
        self.running = False
        self.vc.release()
