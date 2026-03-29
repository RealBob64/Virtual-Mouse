from collections import deque

import pyautogui

class Controller:
    def __init__(self):
        self.prev_pos = None
        self.history = deque(maxlen=5)

    def map_to_screen(self, point):
        screen_width, screen_height = pyautogui.size()
        x = int(point[0] * screen_width)
        y = int(point[1] * screen_height)
        return x, y

    def get_pointer_point(self, landmarks):
        x = (landmarks[9][0] + landmarks[0][0]) / 2
        y = (landmarks[9][1] + landmarks[8][1]) / 2
        return x, y

    def smooth_move(self, x, y):
        if self.prev_pos is None:
            self.prev_pos = x, y

        px, py = self.prev_pos
        dx, dy = x - px, y - py

        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 2:
            return int(px), int(py)

        if dist < 5:
            alpha = 0.1
        elif dist < 20:
            alpha = 0.3
        else:
            alpha = 0.6

        acceleration = min(3, 1 + dist / 50)

        x = px + dx * alpha * acceleration
        y = py + dy * alpha * acceleration

        self.history.append((x, y))
        avg_x = sum(p[0] for p in self.history) / len(self.history)
        avg_y = sum(p[1] for p in self.history) / len(self.history)

        self.prev_pos = avg_x, avg_y

        return int(avg_x), int(avg_y)

    def handle(self, gesture, landmarks):
        if gesture == "MOVE":
            px, py = self.get_pointer_point(landmarks)
            x, y = self.map_to_screen((px, py))
            x, y = self.smooth_move(x, y)
            pyautogui.moveTo(x, y)
        elif gesture == "LEFT_CLICK":
            pyautogui.click(button='left')
        elif gesture == "RIGHT_CLICK":
            pyautogui.click(button='right')
        elif gesture == "SCROLL":
            direction = -1 if landmarks[8][1] < 0.5 else 1
            pyautogui.scroll(100 * direction)
