class Recognizer:
    def __init__(self):
        self.prev_gesture = None
        self.prev_landmarks = None
        self.frame_count = 0

    def distance(self, p1, p2, landmarks):
        x1, y1, _ = landmarks[p1]
        x2, y2, _ = landmarks[p2]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_finger_raised(self, tip, pip, mcp, landmarks):
        return landmarks[tip][1] < landmarks[pip][1] < landmarks[mcp][1]

    def is_holding_mouse(self, landmarks):
        index_fold = self.distance(8, 5, landmarks)
        middle_fold = self.distance(12, 9, landmarks)
        ring_fold = self.distance(16, 13, landmarks)

        return index_fold < 0.15 and middle_fold < 0.15 and ring_fold < 0.15

    def get_vertical_movement(self, landmarks):
        if self.prev_landmarks is None:
            return 0
        return landmarks[8][1] - self.prev_landmarks[8][1]

    def detect_tap(self, tip, thumb, landmarks):
        dist = self.distance(tip, thumb, landmarks)
        return dist < 0.04

    def get_gesture(self, landmarks):
        index_raised = self.is_finger_raised(8, 6, 5, landmarks)
        middle_raised = self.is_finger_raised(12, 10, 9, landmarks)

        vertical_move = self.get_vertical_movement(landmarks)

        gesture = "NONE"

        if self.is_holding_mouse(landmarks):
            gesture = "MOVE"
        elif index_raised and not middle_raised:
            if self.detect_tap(8, 4, landmarks):
                gesture = "RIGHT_CLICK"
            elif abs(vertical_move) > 0.01:
                gesture = "SCROLL"
        elif middle_raised and not index_raised:
            if self.detect_tap(12, 4, landmarks):
                gesture = "LEFT_CLICK"
            elif abs(vertical_move) > 0.01:
                gesture = "SCROLL"
        elif index_raised and middle_raised:
            if abs(vertical_move) > 0.01:
                gesture = "SCROLL"

        self.prev_landmarks = landmarks
        self.prev_gesture = gesture

        return gesture
