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

    def is_finger_down(self, tip, pip, mcp, landmarks):
        return landmarks[tip][1] > landmarks[mcp][1]

    def is_finger_curved(self, tip, pip, mcp, landmarks):
        return landmarks[tip][1] > landmarks[pip][1] > landmarks[mcp][1]

    def is_holding_mouse(self, landmarks):
        #ring_down = self.is_finger_curved(16, 15,13, landmarks)
        #pinky_down = self.is_finger_curved(20, 19, 17, landmarks)
        thumb_fold = self.distance(4, 1, landmarks)
        ring_fold = self.distance(16, 13, landmarks)
        pinky_fold = self.distance(20, 17, landmarks)

        return (thumb_fold < 0.15
                and ring_fold < 0.15 and pinky_fold < 0.15)

    def get_vertical_movement(self, tip, landmarks):
        if self.prev_landmarks is None:
            return 0
        return landmarks[tip][1] - self.prev_landmarks[tip][1]

    def get_gesture(self, landmarks):
        index_raised = self.is_finger_raised(8, 6, 5, landmarks)
        middle_raised = self.is_finger_raised(12, 10, 9, landmarks)
        # index_down = self.is_finger_down(8, 6, 5, landmarks)
        # middle_down = self.is_finger_down(12, 10, 9, landmarks)

        left_vertical_move = self.get_vertical_movement(8, landmarks)
        right_vertical_move = self.get_vertical_movement(12, landmarks)

        index_down = left_vertical_move > 0.02 and self.prev_gesture == "LEFT_UP"
        middle_down = right_vertical_move > 0.02 and self.prev_gesture == "RIGHT_UP"

        is_clicked = self.is_finger_raised(14, 14, 11, landmarks)
        gesture = "NONE"

        if index_raised and not middle_raised:
            self.prev_gesture = "LEFT_UP"
            if index_down:
                gesture = "LEFT_DOWN"
            else:
                gesture = "LEFT_UP"
        elif middle_raised and not index_raised:
            self.prev_gesture = "RIGHT_UP"
            if middle_down:
                gesture = "RIGHT_DOWN"
            else:
                gesture = "RIGHT_UP"
        elif index_raised and middle_raised:
            if abs(left_vertical_move) > 0.01 and abs(right_vertical_move) > 0.01:
                gesture = "SCROLL"
            else:
                gesture = "NONE"
        else:
            gesture = "MOVE"
        '''
        elif self.is_holding_mouse(landmarks):
            gesture = "MOVE"
        else:
            gesture = "NONE"
        '''
        print(gesture)
        self.prev_landmarks = landmarks
        self.prev_gesture = gesture

        return gesture
