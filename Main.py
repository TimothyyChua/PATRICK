import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from PIL import Image, ImageTk

import cv2

import json
import Faces
import Camera
import Sensor
import Telegram
import Speaker

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')

config = load_config('Config.JSON')
Width, Height = config["screen_size"].split('x')
Width = int(Width)
Height = int(Height)

# Placeholder functions for monitoring and statistics
def start_monitoring():
    # Your heart and breathing rate monitoring code here
    pass

def show_statistics():
    # Code to display heart and breathing rate statistics
    pass

def switch_face(canvas, face_style):
    # Placeholder function for switching face styles
    canvas.delete("all")

def clear_canvas(elements):
    for widget in elements:
        widget.destroy()
        
def set_operation_mode(mode):
    # Placeholder function for setting operation mode
    pass

def set_monitoring_interval(interval):
    # Placeholder function for setting monitoring interval
    pass

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

# Main application class
class RobotUI(tk.Tk):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #elf.parent = parent
        self.title("Friendly Robot")
        self.geometry(config["screen_size"])
        self.configure(bg='black')
        
        self.settings = config["settings"]
        self.states = config["states"]
        self.images = config["images"]
        
        self.camera = Camera.CameraHandler(self)
        self.sensorHandler = None
        self.telegram = Telegram.TelegramBot()
        self.feed_sound = Speaker.AudioPlayer(config["sounds"]["feed_sound"], 5.0)

        # Placeholder images
        self.placeholder_image = PhotoImage(width=40, height=40)  # Placeholder image size 40x40
        self.create_placeholder_image(self.placeholder_image)

        # Load specific images if available
        self.back_image = self.load_image(self.images["back_button"]) or self.placeholder_image
        self.face_image = self.load_image(self.images["face_button"]) or self.placeholder_image
        self.settings_image = self.load_image(self.images["settings_button"]) or self.placeholder_image
        
        self.hr_image = self.load_image(self.images["hr_image"]) or self.placeholder_image
        self.br_image = self.load_image(self.images["br_image"]) or self.placeholder_image

        # Main layout frame
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(expand=True, fill='both')
        
        # Left side menu buttons
        self.menu_frame = tk.Frame(self.main_frame, width=80, bg='black')
        self.menu_frame.pack(side="left", fill='y')

        back_button = tk.Button(self.menu_frame, command=self.default_face_screen, bg='black', fg='white')
        back_button.pack(pady=5, fill='x')
        self.set_button_image(back_button, self.back_image, 40, 40)
        
        face_button = tk.Button(self.menu_frame, command=self.show_face_settings, bg='black', fg='white')
        face_button.pack(pady=5, fill='x')
        self.set_button_image(face_button, self.face_image, 40, 40)
        
        mode_button = tk.Button(self.menu_frame, command=self.show_mode_settings, bg='black', fg='white')
        mode_button.pack(pady=5, fill='x')
        self.set_button_image(mode_button, self.settings_image, 40, 40)

        # Right side sub-settings frame
        self.sub_settings_frame = tk.Frame(self.main_frame, relief=tk.RIDGE, borderwidth=2, bg='black')
        self.sub_settings_frame.pack(side="top", expand=True, fill='both')

        # Bottom buttons
        bottom_frame = tk.Frame(self.main_frame, bg='black')
        bottom_frame.pack(side="bottom", fill='x')

        camera_button = tk.Button(bottom_frame, text="Camera View", command=self.show_camera_view, bg='black', fg='white')
        camera_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')

        stats_button = tk.Button(bottom_frame, text="Show Statistics", command=self.show_statistics_screen, bg='black', fg='white')
        stats_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')

        # self.ball_state = self.states["ball_state"]
        #self.ball_button = tk.Button(bottom_frame, text="Ball", command=self.toggle_ball_state, bg='black', fg='white')
        #self.ball_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')
        #self.update_ball_button()

        self.feed_button = tk.Button(bottom_frame, text="Feed", command=self.update_feed, bg='black', fg='white')
        self.feed_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')
        self.feed_count = 0
        #self.update_ball_button()

        # Initialize the canvas properly
        self.canvas = ScalableCanvas(self, width=200, height=200, bg='black')
        self.canvas.pack(expand=True, fill='both')
        
        self.default_face_screen()

    def create_placeholder_image(self, image):
        """ Creates a simple placeholder image with a cross """
        width, height = 40, 40
        image.put("white", to=(0, 0, width, height))
        for i in range(0, width, 2):
            image.put("black", to=(i, i, i+1, i+1))
            image.put("black", to=(width-i-1, i, width-i, i+1))

    def load_image(self, image_name):
        """ Load an image if it exists """
        try:
            return PhotoImage(file=f"{image_name}.png")
        except tk.TclError:
            return None

    def set_button_image(self, button, image, width, height):
        """ Scale and set an image on a button """
        scaled_image = self.scale_image(image, width, height)
        button.config(image=scaled_image)
        button.image = scaled_image

    def scale_image(self, image, width, height):
        """ Scale an image to fit within the given width and height """
        return image.subsample(max(image.width() // width, 1), max(image.height() // height, 1))

    def toggle_ball_state(self):
        #self.states["ball_state"] = not self.states["ball_state"]
        self.update_ball_button()
        
    def update_ball_button(self):
        if self.states["ball_state"]:
            self.ball_button.config(highlightbackground="green", highlightthickness=2, bg="green")
        else:
            self.ball_button.config(highlightbackground="black", highlightthickness=1, bg="black")

    def update_feed(self):
        self.feed_count += 1
        print(self.feed_count)
        if not self.feed_sound.is_playing():
            self.feed_sound.play()
        pass

    def default_face_screen(self):
        clear_canvas(self.winfo_children())
        
        # Initialize the canvas properly
        self.canvas = ScalableCanvas(self, width=200, height=200, bg='black')
        self.canvas.pack(expand=True, fill='both')

        self.canvas.bind("<Button-1>", self.show_main_menu)
        
        self.display_face = Faces.RobotFace(self.canvas, expression=self.settings["face_style"])
        self.display_face.update()

    def show_main_menu(self, event=None):
        clear_canvas(self.winfo_children())  
        
        # Recreate main layout frame
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(expand=True, fill='both')

        # Left side menu buttons
        self.menu_frame = tk.Frame(self.main_frame, width=80, bg='black')
        self.menu_frame.pack(side="left", fill='y')

        back_button = tk.Button(self.menu_frame, command=self.default_face_screen, bg='black', fg='white')
        back_button.pack(pady=5, fill='x')
        self.set_button_image(back_button, self.back_image, 40, 40)
        
        face_button = tk.Button(self.menu_frame, command=self.show_face_settings, bg='black', fg='white')
        face_button.pack(pady=5, fill='x')
        self.set_button_image(face_button, self.face_image, 40, 40)
        
        mode_button = tk.Button(self.menu_frame, command=self.show_mode_settings, bg='black', fg='white')
        mode_button.pack(pady=5, fill='x')
        self.set_button_image(mode_button, self.settings_image, 40, 40)

        # Right side sub-settings frame
        self.sub_settings_frame = tk.Frame(self.main_frame, relief=tk.RIDGE, borderwidth=2, bg='black')
        self.sub_settings_frame.pack(side="top", expand=True, fill='both')

        # Bottom buttons
        bottom_frame = tk.Frame(self.main_frame, bg='black')
        bottom_frame.pack(side="bottom", fill='x')

        camera_button = tk.Button(bottom_frame, text="Camera View", command=self.show_camera_view, bg='black', fg='white')
        camera_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')

        stats_button = tk.Button(bottom_frame, text="Show Statistics", command=self.show_statistics_screen, bg='black', fg='white')
        stats_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')

        #self.ball_button = tk.Button(bottom_frame, text="Ball", command=self.toggle_ball_state, bg='black', fg='white')
        #self.ball_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')
        #self.update_ball_button()
        
        self.feed_button = tk.Button(bottom_frame, text="Feed", command=self.update_feed, bg='black', fg='white')
        self.feed_button.pack(side="left", padx=5, pady=5, expand=True, fill='x')

    def show_face_settings(self):
        clear_canvas(self.sub_settings_frame.winfo_children())  

        self.face_options = [
            (self.images["face1"], "Happy", "1"),
            (self.images["face2"], "Sad", "2"),
            (self.images["face3"], "Surprised", "3"),
            (self.images["face4"], "Crossed", "4")
        ]

        self.current_page = 0
        self.total_pages = (len(self.face_options) + 1) // 2

        face_settings_menu = tk.Frame(self.sub_settings_frame, bg='black')
        face_settings_menu.grid(row=0, column=0, sticky='nsew')

        self.face_frames = [tk.Frame(face_settings_menu, bg='black') for _ in range(self.total_pages)]
        for i, frame in enumerate(self.face_frames):
            frame.grid(row=0, column=0, sticky='nsew')

        prev_button = tk.Button(face_settings_menu, text="Previous", command=self.previous_page, bg='black', fg='white')
        prev_button.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        next_button = tk.Button(face_settings_menu, text="Next", command=self.next_page, bg='black', fg='white')
        next_button.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        self.update_face_settings_page()

    def update_face_settings_page(self):
        for frame in self.face_frames:
            clear_canvas(frame.winfo_children())

        start_index = self.current_page * 2
        for i, face in enumerate(self.face_options[start_index:start_index + 2]):
            face_image = self.load_image(face[0]) or self.placeholder_image
            face_image = self.scale_image(face_image, 80, 80)  # Scale the image to fit
            face_frame_item = tk.Frame(self.face_frames[self.current_page], padx=5, pady=5, relief=tk.RIDGE, borderwidth=2, bg='black')
            face_frame_item.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            face_label = tk.Label(face_frame_item, image=face_image, bg='black')
            face_label.image = face_image  # Keep a reference to avoid garbage collection
            face_label.pack(expand=True, fill='both')
            tk.Label(face_frame_item, text=face[1], bg='black', fg='white').pack()
            tk.Button(face_frame_item, text="Select", command=lambda s=face[2], m=face[1]: self.set_face_style(s, m), bg='black', fg='white').pack()

        self.face_frames[self.current_page].tkraise()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_face_settings_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_face_settings_page()

    def set_face_style(self, style=None, mood=None):
        self.settings["face_style"] = style
        self.display_face.expression = style
        
        #Send telegram message
        if style and mood:
            self.telegram.send_message(f"User is feeling {str(mood)}")
        
        #switch_face(self.canvas, style)

    def show_mode_settings(self):
        clear_canvas(self.sub_settings_frame.winfo_children())
        mode_settings_menu = tk.Frame(self.sub_settings_frame, bg='black')
        mode_settings_menu.pack(expand=True)
        
        # Operation mode text
        tk.Label(mode_settings_menu, text="Mode", bg='black', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        # Drop-down menu for operation mode
        mode_var = tk.StringVar(value=self.settings["operation_mode"])
        mode_menu = ttk.Combobox(mode_settings_menu, textvariable=mode_var, values=["Interval", "Continuous"])
        mode_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Monitoring interval option
        interval_label = tk.Label(mode_settings_menu, text="Interval", bg='black', fg='white')
        interval_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        interval_label.config(state=tk.NORMAL if self.settings["operation_mode"] == "Interval" else tk.DISABLED)

        interval_value = tk.StringVar(value=f"{self.settings['monitoring_interval']} hrs")
        interval_slider = ttk.Scale(mode_settings_menu, from_=0.5, to=24, orient=tk.HORIZONTAL, command=lambda val: interval_value.set(f"{float(val):.1f} hrs"))
        interval_slider.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        interval_slider.set(self.settings["monitoring_interval"])
        interval_slider.state(["!disabled"] if self.settings["operation_mode"] == "Interval" else ["disabled"])

        interval_value_label = tk.Label(mode_settings_menu, textvariable=interval_value, bg='black', fg='white')
        interval_value_label.grid(row=1, column=1, padx=110, pady=10, sticky='w')

        def update_interval_options(event):
            if mode_var.get() == "Interval":
                interval_label.config(state=tk.NORMAL)
                interval_slider.state(["!disabled"])
                interval_value_label.config(state=tk.NORMAL)
            else:
                interval_label.config(state=tk.DISABLED)
                interval_slider.state(["disabled"])
                interval_value_label.config(state=tk.DISABLED)
            self.settings["operation_mode"] = mode_var.get()

        def update_interval_value(val):
            rounded_val = round(float(val) * 2) / 2  # Round to nearest 0.5
            interval_value.set(f"{rounded_val:.1f} hrs")
            self.settings["monitoring_interval"] = rounded_val

        mode_menu.bind("<<ComboboxSelected>>", update_interval_options)
        interval_slider.config(command=update_interval_value)

    def show_camera_view(self):
        clear_canvas(self.winfo_children())
        
        # Create a frame to hold the top buttons
        top_frame = tk.Frame(self, bg='black')
        top_frame.pack(side="top", fill='x')

        back_button = tk.Button(top_frame, text="Back", command=self.show_main_menu, bg='black', fg='white')
        back_button.pack(side="left", pady=5)
        self.set_button_image(back_button, self.back_image, 40, 40)
        
        self.camera_toggle_button = tk.Button(top_frame, text="Camera", command=self.toggle_camera_state, bg='black', fg='white')
        self.camera_toggle_button.pack(side="left", padx=5, pady=5)

        self.update_camera_text()
       
    def toggle_camera_state(self):
        self.states["camera_state"] = not self.states["camera_state"]
        self.update_camera_text()

    def update_camera_text(self):
        if self.states["camera_state"]:
            self.camera_toggle_button.config(highlightbackground="green", highlightthickness=2, bg="green")
            if hasattr(self, 'camera_canvas'):
                self.camera_canvas.destroy()
            self.camera_canvas = ScalableCanvas(self, width=200, height=200, bg='black')
            self.camera_canvas.pack(expand=True, fill='both')
            self.camera.open_camera()
            self.update_camera_display(self.camera_canvas)
        else:
            self.camera.close_camera()
            self.camera_toggle_button.config(highlightbackground="black", highlightthickness=1, bg="black")
            # Clear the canvas and display "Camera is off"
            if hasattr(self, 'camera_canvas'):
                self.camera_canvas.destroy()
            self.camera_canvas = tk.Label(self, text="Camera is off", font=("Helvetica", 24), bg='black', fg='white')
            self.camera_canvas.pack(expand=True, fill='both')
            
    def update_camera_display(self, canvas):
        if self.camera.is_opened():
            frame = self.camera.get_frame()
            frame = cv2.resize(frame, (Width, Height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)

            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo  # Prevent garbage collection of the image
            self.after(17, self.update_camera_display, canvas)

    def on_closing(self):
        self.camera.close_camera()
        self.destroy()

    def show_statistics_screen(self):
        clear_canvas(self.winfo_children())
        #start_monitoring()
        #show_statistics()
        
        top_frame = tk.Frame(self, bg='black')
        top_frame.pack(side="top", fill='x')

        back_button = tk.Button(top_frame, text="Back", command=self.default_face_screen, bg='black', fg='white')
        back_button.pack(side="left", pady=5)
        self.set_button_image(back_button, self.back_image, 40, 40)
        
        stats_frame = tk.Frame(self)
        stats_frame.pack(fill='x', pady=10)

        hr_frame = tk.Frame(stats_frame, bg='black')
        hr_frame.pack(fill='x', pady=5)
        
        br_frame = tk.Frame(stats_frame, bg='black')
        br_frame.pack(fill='x', pady=5)
        
        # Heart rate label
        heartrate_image_label = tk.Label(hr_frame, image=self.hr_image, bg='black')
        heartrate_image_label.pack(side="left", padx=10)
        self.set_button_image(heartrate_image_label, self.hr_image, 80, 80)
        
        self.heartrate_label = tk.Label(hr_frame, text="Heart Rate: ", font=("Helvetica", 16), bg='black', fg='white')
        self.heartrate_label.pack(side="left", padx=10)

        # Breath rate label
        breathrate_image_label = tk.Label(br_frame, image=self.br_image, bg='black')
        breathrate_image_label.pack(side="left", padx=10)
        self.set_button_image(breathrate_image_label, self.br_image, 80, 80)
        
        self.breathrate_label = tk.Label(br_frame, text="Breath Rate: ", font=("Helvetica", 16), bg='black', fg='white')
        self.breathrate_label.pack(side="left", padx=10)
        
        self.start_monitor_button = tk.Button(top_frame, text="Toggle", command=self.toggle_monitoring_state, bg='black', fg='white')
        self.start_monitor_button.pack(side="left", pady=5)
        
        #self.update_monitoring()

    def toggle_monitoring_state(self):
        self.states["monitoring_state"] = not self.states["monitoring_state"]
        
        if self.states["monitoring_state"]:
            self.start_monitor_button.config(highlightbackground="green", highlightthickness=2, bg="green")
            self.sensorHandler = Sensor.SensorHandler(self)
        else:
            self.start_monitor_button.config(highlightbackground="black", highlightthickness=1, bg="black")
        self.update_monitoring()
        
            
    def update_monitoring(self):
        if self.states["monitoring_state"]:
            self.sensorHandler.read_line()
            self.heartrate_label.config(text=f"Heart Rate: {self.sensorHandler.heartrate}")
            self.breathrate_label.config(text=f"Breath Rate: {self.sensorHandler.breathrate}")
            self.after(1000, self.update_monitoring)
        else:
            self.sensorHandler.stop()


if __name__ == "__main__":
    #root = tk.Tk()
    app = RobotUI()
    app.attributes("-fullscreen",True)
    app.mainloop()
