import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

vc = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while vc.isOpened():
        read_success, frame = vc.read()
        if not read_success:
            break

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_hands = hands.process(frame)

        if detected_hands.multi_hand_landmarks:
            for hands_landmarks in detected_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hands_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

vc.release()
cv2.destroyWindow('Video')