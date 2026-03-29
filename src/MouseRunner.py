import mediapipe as mp
import MouseController
import MouseRecognizer
import cv2

vc = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

controller = MouseController.Controller()
recognizer = MouseRecognizer.Recognizer()

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while vc.isOpened():
        read_success, frame = vc.read()
        if not read_success:
            break

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                gesture = recognizer.get_gesture(landmarks)
                controller.handle(gesture, landmarks)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

vc.release()
cv2.destroyWindow('Video')