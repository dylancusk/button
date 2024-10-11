import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import datetime
import csv
import RPi.GPIO as GPIO

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.image_folder = None
        self.image_files = []
        self.image_index = 0
        self.display_label = tk.Label(root)
        self.display_label.pack()
        self.log = []

        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack()

        # Setup GPIO for physical button
        self.gpio_button_pin = 17  # GPIO pin number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio_button_pin, GPIO.FALLING, callback=self.gpio_button_pressed, bouncetime=300)

    def select_folder(self):
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            self.image_index = 0
            self.next_image()

    def next_image(self):
        if self.image_files:
            image_path = os.path.join(self.image_folder, self.image_files[self.image_index])
            image = Image.open(image_path)
            # Resize image if necessary to fit the screen
            image = image.resize((320, 240), Image.ANTIALIAS)  # Adjust size as needed
            photo = ImageTk.PhotoImage(image)
            self.display_label.config(image=photo)
            self.display_label.image = photo  # Keep a reference to avoid garbage collection
            self.current_image_name = self.image_files[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.image_files)
            self.root.after(5000, self.next_image)

    def record_image(self):
        if self.image_files:
            image_path = os.path.join(self.image_folder, self.image_files[self.image_index])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append((image_path, timestamp))
            with open('image_log.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([image_path, timestamp])
            self.image_index = (self.image_index + 1) % len(self.image_files)
            self.next_image()

    def gpio_button_pressed(self, channel):
        self.root.after(0, self.record_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.mainloop()
    GPIO.cleanup()