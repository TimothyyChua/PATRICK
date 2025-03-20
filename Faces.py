import tkinter as tk
import sys
import math
from tkinter import Tk, Canvas

import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')
Width, Height = config["screen_size"].split('x')
Width = int(Width)
Height = int(Height)

class RobotFace():
    def __init__(self, canvas, expression="1", width=Width, height=Height, fps=60):
        #pygame.init()
        try:
            self.expression = str(expression)
        except ValueError:
            raise ValueError("The expression parameter must be a valid string")
        
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = width, height
        self.FPS = 60
        self.FACE_POSITION = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        self.EYE_RADIUS = 20
        self.EYE_OFFSET = 60
        self.MOUTH_WIDTH = 160
        self.MOUTH_HEIGHT = 40
        self.MAX_TIME = 2 * math.pi

        self.canvas = canvas
        self.time = 0
        self.expression = expression
        self.running = True
        
    def draw_happy_face(self, smile_intensity, eye_intensity):
        self.canvas.delete("all")
        dynamic_eye_radius = self.EYE_RADIUS + 2 * math.sin(eye_intensity)
        # Left eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] - self.EYE_OFFSET - dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 - dynamic_eye_radius, 
            self.FACE_POSITION[0] - self.EYE_OFFSET + dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 + dynamic_eye_radius, 
            fill='white'
        )
        # Right eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] + self.EYE_OFFSET - dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 - dynamic_eye_radius, 
            self.FACE_POSITION[0] + self.EYE_OFFSET + dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 + dynamic_eye_radius, 
            fill='white'
        )
        smile_offset = 20 + 10 * math.sin(smile_intensity)
        # Mouth
        self.canvas.create_arc(
            self.FACE_POSITION[0] - self.MOUTH_WIDTH // 2, 
            self.FACE_POSITION[1] + smile_offset, 
            self.FACE_POSITION[0] + self.MOUTH_WIDTH // 2, 
            self.FACE_POSITION[1] + smile_offset + self.MOUTH_HEIGHT, 
            start=0, extent=-180, style='arc', outline='white', width=5
        )

    def draw_sad_face(self, smile_intensity, eye_intensity):
        self.canvas.delete("all")
        eye_vertical_movement = 5 * math.sin(eye_intensity)
        # Left eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] - self.EYE_OFFSET - self.EYE_RADIUS, 
            self.FACE_POSITION[1] - 20 + eye_vertical_movement - self.EYE_RADIUS, 
            self.FACE_POSITION[0] - self.EYE_OFFSET + self.EYE_RADIUS, 
            self.FACE_POSITION[1] - 20 + eye_vertical_movement + self.EYE_RADIUS, 
            fill='white'
        )
        # Right eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] + self.EYE_OFFSET - self.EYE_RADIUS, 
            self.FACE_POSITION[1] - 20 + eye_vertical_movement - self.EYE_RADIUS, 
            self.FACE_POSITION[0] + self.EYE_OFFSET + self.EYE_RADIUS, 
            self.FACE_POSITION[1] - 20 + eye_vertical_movement + self.EYE_RADIUS, 
            fill='white'
        )
        mouth_start = (self.FACE_POSITION[0] - self.MOUTH_WIDTH // 2, self.FACE_POSITION[1] + 50)
        mouth_end = (self.FACE_POSITION[0] + self.MOUTH_WIDTH // 2, self.FACE_POSITION[1] + 50 + self.MOUTH_HEIGHT)
        self.canvas.create_arc(
            mouth_start[0], mouth_start[1], mouth_end[0], mouth_end[1], 
            start=0, extent=180 + 10 * math.sin(smile_intensity), style='arc', outline='white', width=5
        )

    def draw_surprised_face(self, smile_intensity, eye_intensity):
        self.canvas.delete("all")
        eye_height = 40 + 10 * math.sin(eye_intensity)
        # Left eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] - self.EYE_OFFSET - 20, 
            self.FACE_POSITION[1] - 30, 
            self.FACE_POSITION[0] - self.EYE_OFFSET + 20, 
            self.FACE_POSITION[1] - 30 + eye_height, 
            fill='white'
        )
        # Right eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] + self.EYE_OFFSET - 20, 
            self.FACE_POSITION[1] - 30, 
            self.FACE_POSITION[0] + self.EYE_OFFSET + 20, 
            self.FACE_POSITION[1] - 30 + eye_height, 
            fill='white'
        )
        mouth_width = self.MOUTH_WIDTH // 2 + 10 * math.sin(smile_intensity)
        mouth_height = self.MOUTH_HEIGHT // 2 + 10 * math.sin(smile_intensity)
        # Mouth
        self.canvas.create_oval(
            self.FACE_POSITION[0] - mouth_width // 2, 
            self.FACE_POSITION[1] + 40, 
            self.FACE_POSITION[0] + mouth_width // 2, 
            self.FACE_POSITION[1] + 40 + mouth_height, 
            outline='white', width=5
        )

    def draw_crossed_eyes_face(self, smile_intensity, eye_intensity):
        self.canvas.delete("all")
        eye_size = 40 + 5 * math.sin(eye_intensity)
        # Left eye
        self.canvas.create_line(
            self.FACE_POSITION[0] - self.EYE_OFFSET - eye_size // 4, 
            self.FACE_POSITION[1] - 20 - eye_size // 4,
            self.FACE_POSITION[0] - self.EYE_OFFSET + eye_size // 4, 
            self.FACE_POSITION[1] - 20 + eye_size // 4, 
            fill='white', width=5
        )
        self.canvas.create_line(
            self.FACE_POSITION[0] - self.EYE_OFFSET + eye_size // 4, 
            self.FACE_POSITION[1] - 20 - eye_size // 4,
            self.FACE_POSITION[0] - self.EYE_OFFSET - eye_size // 4, 
            self.FACE_POSITION[1] - 20 + eye_size // 4, 
            fill='white', width=5
        )
        # Right eye
        self.canvas.create_line(
            self.FACE_POSITION[0] + self.EYE_OFFSET - eye_size // 4, 
            self.FACE_POSITION[1] - 20 - eye_size // 4,
            self.FACE_POSITION[0] + self.EYE_OFFSET + eye_size // 4, 
            self.FACE_POSITION[1] - 20 + eye_size // 4, 
            fill='white', width=5
        )
        self.canvas.create_line(
            self.FACE_POSITION[0] + self.EYE_OFFSET + eye_size // 4, 
            self.FACE_POSITION[1] - 20 - eye_size // 4,
            self.FACE_POSITION[0] + self.EYE_OFFSET - eye_size // 4, 
            self.FACE_POSITION[1] - 20 + eye_size // 4, 
            fill='white', width=5
        )
        mouth_width = self.MOUTH_WIDTH // 1.5 + 20 * math.sin(smile_intensity)
        mouth_height = self.MOUTH_HEIGHT // 10
        mouth_movement = 3 * math.sin(smile_intensity)
        self.canvas.create_rectangle(
            self.FACE_POSITION[0] - mouth_width // 2, 
            self.FACE_POSITION[1] + 40 + mouth_movement, 
            self.FACE_POSITION[0] + mouth_width // 2, 
            self.FACE_POSITION[1] + 40 + mouth_movement + mouth_height, 
            outline='white', width=5
        )

    def draw_winking_face_2(self, smile_intensity, eye_intensity):
        self.canvas.delete("all")
        dynamic_eye_radius = self.EYE_RADIUS + 2 * math.sin(eye_intensity)
        # Left eye
        self.canvas.create_oval(
            self.FACE_POSITION[0] - self.EYE_OFFSET - dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 - dynamic_eye_radius, 
            self.FACE_POSITION[0] - self.EYE_OFFSET + dynamic_eye_radius, 
            self.FACE_POSITION[1] - 20 + dynamic_eye_radius, 
            fill='white'
        )
        eye_height = self.EYE_RADIUS - self.EYE_RADIUS * math.sin(eye_intensity)
        if eye_height > self.EYE_RADIUS:
            eye_height = dynamic_eye_radius
        # Right eye (winking)
        self.canvas.create_oval(
            self.FACE_POSITION[0] + self.EYE_OFFSET - dynamic_eye_radius, 
            self.FACE_POSITION[1] - 35, 
            self.FACE_POSITION[0] + self.EYE_OFFSET + dynamic_eye_radius, 
            self.FACE_POSITION[1] - 35 + eye_height, 
            fill='white'
        )
        mouth_width = self.MOUTH_WIDTH // 2
        mouth_height = self.MOUTH_HEIGHT // 2
        # Mouth
        self.canvas.create_arc(
            self.FACE_POSITION[0] - mouth_width // 2, 
            self.FACE_POSITION[1] + 40, 
            self.FACE_POSITION[0] + mouth_width // 2, 
            self.FACE_POSITION[1] + 40 + mouth_height, 
            start=0, extent=-180, style='arc', outline='white', width=5
        )


    def stop(self):
        self.running = False

    def update(self):
        if not self.running:
            return
        self.time += 0.05
        if self.time >= self.MAX_TIME:
            self.time = 0

        smile_intensity = self.time
        eye_intensity = self.time * 2

        if self.expression == "1":
            self.draw_happy_face(smile_intensity, eye_intensity)
        elif self.expression == "2":
            self.draw_sad_face(smile_intensity, eye_intensity)
        elif self.expression == "3":
            self.draw_surprised_face(smile_intensity, eye_intensity)
        elif self.expression == "4":
            self.draw_crossed_eyes_face(smile_intensity, eye_intensity)
        elif self.expression == "5":
            self.draw_winking_face_2(smile_intensity, eye_intensity)

        self.canvas.after(int(1000 / self.FPS), self.update)


class ScalableCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

    def on_resize(self, event):
        scale_x = event.width / self.width
        scale_y = event.height / self.height
        self.width = event.width
        self.height = event.height
        self.scale("all", 0, 0, scale_x, scale_y)

