import tkinter as tk
from tkinter import messagebox

#import Telegram

class PopupWindow:
    def __init__(self, parent, message="Are You Alright?", bg_color="#333333", fg_color="#FFFFFF"):
        self.parent = parent
        self.message = message
        self.response = None
        self.bg_color = bg_color
        self.fg_color = fg_color
        #self.telegram = Telegram.TelegramBot()

    def on_yes(self):
        self.response = "Yes"
        #messagebox.showinfo("Response", "You clicked Yes!")
        self.popup.destroy()

    def on_no(self):
        self.response = "No"
        #messagebox.showinfo("Response", "You clicked No!")
        self.popup.destroy()
    
    def on_click(self, resp):
        self.response = resp
        x = resp
        if resp == "Yes":
            x = "Okay"
        else:
            x = "Not Okay"
        #self.telegram.send_message(f"User is {x}!")
        self.popup.destroy()

    def show(self):
        # Create the pop-up window
        self.popup = tk.Toplevel(self.parent)
        #self.popup.title("Question")
        self.popup.geometry("600x300")
        self.popup.attributes('-topmost', True)  # Keep the window on top
        self.popup.configure(bg=self.bg_color)

        # Create the question label
        label = tk.Label(self.popup, text=self.message, font=("Arial", 12), bg=self.bg_color, fg=self.fg_color)
        label.pack(pady=20)

        # Create the Yes and No buttons
        yes_button = tk.Button(self.popup, text="Yes", command=lambda resp="Yes": self.on_click(resp), width=10, bg=self.bg_color, fg=self.fg_color, highlightbackground=self.bg_color)
        yes_button.pack(side=tk.LEFT, padx=20, pady=20)

        no_button = tk.Button(self.popup, text="No", command=lambda resp="No": self.on_click(resp), width=10, bg=self.bg_color, fg=self.fg_color, highlightbackground=self.bg_color)
        no_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Wait for the window to close
        self.parent.wait_window(self.popup)

        return self.response

# Example of another class that calls the PopupWindow

class ExampleClass:
    def __init__(self, parent):
        self.parent = parent

    def perform_action(self):
        popup = PopupWindow(self.parent)
        result = popup.show()
        if result == "Yes":
            print("Action confirmed.")
        else:
            print("Action canceled.")

# Main application
def main():
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("400x300")
    root.configure(bg="#333333")  # Set dark mode background color

    # Example of integrating the popup in the main application
    example = ExampleClass(root)
    button = tk.Button(root, text="Show Popup", command=example.perform_action, bg="#555555", fg="#FFFFFF")
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
