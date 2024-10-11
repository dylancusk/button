import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import datetime
import csv

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
        
        self.save_button = tk.Button(root, text="Record Image", command=self.record_image, state=tk.DISABLED)
        self.save_button.pack()

    def select_folder(self):
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            self.image_index = 0
            self.save_button.config(state=tk.NORMAL)
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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append((self.current_image_name, timestamp, self.save_button_press_count))
        print(f"Recorded: {self.current_image_name} at {timestamp} with {self.save_button_press_count} button press(es)")

        # Save log as CSV
        csv_file = os.path.join(self.image_folder, "log.csv")
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Image Name", "Timestamp", "Button Press Count"])
            writer.writerows(self.log)

    def increment_button_press_count(self):
        self.save_button_press_count += 1

    def select_folder(self):
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            self.image_index = 0
            self.save_button.config(state=tk.NORMAL)
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
            self.save_button_press_count = 0  # Reset button press count for each new image
            self.root.after(5000, self.next_image)

    def record_image(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append((self.current_image_name, timestamp, self.save_button_press_count))
        print(f"Recorded: {self.current_image_name} at {timestamp} with {self.save_button_press_count} button press(es)")

        # Save log as CSV
        csv_file = os.path.join(self.image_folder, "log.csv")
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Image Name", "Timestamp", "Button Press Count"])
            writer.writerows(self.log)

    def increment_button_press_count(self):
        self.save_button_press_count += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    root.mainloop()