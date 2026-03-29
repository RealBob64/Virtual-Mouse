import pyautogui

class Controller:
    def __init__(self):
        self.prev_pos = None

    def map_to_screen(self, point):
        screen_width, screen_height = pyautogui.size()
        x = int(point[0] * screen_width)
        y = int(point[1] * screen_height)
        return x, y

    def smooth_move(self, x, y):
        if self.prev_pos is None:
            self.prev_pos = x, y

        px, py = self.prev_pos

        x = int(px + (x - px) * 0.3)
        y = int(py + (y - py) * 0.3)
        self.prev_pos = (x, y)
        return x, y

    def handle(self, gesture, landmarks):
        if gesture == "MOVE":
            x, y = self.map_to_screen(landmarks[9])
            x, y = self.smooth_move(x, y)
            pyautogui.moveTo(x, y)
        elif gesture == "LEFT_CLICK":
            pyautogui.click(button='left')
        elif gesture == "RIGHT_CLICK":
            pyautogui.click(button='right')
        elif gesture == "SCROLL":
            direction = -1 if landmarks[8][1] < 0.5 else 1
            pyautogui.scroll(100 * direction)
