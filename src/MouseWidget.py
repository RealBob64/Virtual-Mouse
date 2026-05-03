from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
from math import cos, sin, pi


class MouseWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.left_active = False
        self.right_active = False
        self.scroll_active = False

    def initializeGL(self):
        glClearColor(0.08, 0.08, 0.1, 1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        self.draw_body()
        self.draw_buttons()
        self.draw_scroll()
        self.draw_divider()

    def draw_body(self):
        # soft gradient (fake 3D)
        for i in range(20):
            t = i / 20
            shade = 0.6 + 0.2 * (1 - t)
            glColor3f(shade, shade, shade)
            self.draw_ellipse(0, -0.05 * t, 0.55 - 0.02*t, 0.85 - 0.02*t)

        # highlight
        glColor3f(0.9, 0.9, 0.95)
        self.draw_ellipse(0, 0.25, 0.35, 0.25)

    def draw_buttons(self):
        # left button
        if self.left_active:
            glColor3f(1, 0.2, 0.2)
        else:
            glColor3f(0.82, 0.82, 0.85)

        self.draw_button_shape(-0.275, 0.2, 0.275, 0.75)

        # right button
        if self.right_active:
            glColor3f(1, 0.2, 0.2)
        else:
            glColor3f(0.82, 0.82, 0.85)

        self.draw_button_shape(0.275, 0.2, -0.275, 0.75, flip=True)

    def draw_scroll(self):
        if self.scroll_active:
            glColor3f(1, 1, 0.2)
        else:
            glColor3f(0.2, 0.2, 0.25)

        self.draw_ellipse(0, 0.25, 0.07, 0.18)

    def draw_divider(self):
        glColor3f(0.3, 0.3, 0.35)
        glLineWidth(2)

        glBegin(GL_LINES)
        glVertex2f(0, 0.75)
        glVertex2f(0, -0.1)
        glEnd()

    def draw_ellipse(self, cx, cy, rx, ry):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)

        for i in range(100):
            angle = 2 * pi * i / 100
            glVertex2f(cx + rx * cos(angle), cy + ry * sin(angle))

        glEnd()

    def draw_button_shape(self, cx, cy, rx, ry, flip=False):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)

        start = pi/2
        end = pi

        if flip:
            start = 0
            end = pi/2

        for i in range(50):
            t = i / 50
            angle = start + (end - start) * t
            x = cx + rx * cos(angle)
            y = cy + ry * sin(angle)
            glVertex2f(x, y)

        # extend down to match body
        glVertex2f(cx + (rx if not flip else -rx), -0.1)
        glVertex2f(cx, -0.1)

        glEnd()

    def update_state(self, gesture):
        self.left_active = False
        self.right_active = False
        self.scroll_active = False

        if gesture == "LEFT_CLICK":
            self.left_active = True
        elif gesture == "RIGHT_CLICK":
            self.right_active = True
        elif gesture == "SCROLL":
            self.scroll_active = True

        self.update()