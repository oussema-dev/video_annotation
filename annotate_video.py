import cv2
import tkinter as tk
from tkinter import filedialog
import csv
from PIL import Image, ImageTk
import os


class VideoPlayer:
    def __init__(self, root, button_names):
        self.root = root
        self.root.title("Annotate Video")
        self.video_file = None
        self.cap = None
        self.frame_number = 0
        self.frame_total = 0
        self.play = False
        # Initialize frame skip to 1 (normal speed)
        self.frame_skip = 1
        self.buttons = button_names
        self.button_states = {}
        # Initialize a list to store frame data (list is better than dict to have sorted data by precedence)
        self.frame_data_list = []

        self.create_widgets()
        self.update_frame()

    def create_widgets(self):
        
        # Left part (video canvas and standard buttons)
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT)

        # Display the video name at the top-left corner
        video_name_frame = tk.Frame(left_frame)
        video_name_frame.pack(anchor=tk.NW, padx=10, pady=10)

        self.video_name_label = tk.Label(
            video_name_frame, text="", font=("Helvetica", 14)
        )
        self.video_name_label.pack()

        self.canvas = tk.Canvas(left_frame, width=720, height=480)
        self.canvas.pack()

        self.button_frame = tk.Frame(left_frame)
        self.button_frame.pack()

        self.elapsed_time_label = tk.Label(
            self.button_frame, text="Elapsed Time: 00:00:000", font=("Helvetica", 12)
        )
        self.elapsed_time_label.grid(row=0, column=0, padx=10, pady=5)

        self.play_button = tk.Button(
            self.button_frame, text="Play", command=self.toggle_play
        )
        self.play_button.grid(row=0, column=1, padx=5, pady=5)

        self.prev_button = tk.Button(
            self.button_frame, text="Previous Frame", command=self.prev_frame
        )
        self.prev_button.grid(row=0, column=2, padx=5, pady=5)

        self.next_button = tk.Button(
            self.button_frame, text="Next Frame", command=self.next_frame
        )
        self.next_button.grid(row=0, column=3, padx=5, pady=5)

        self.save_button = tk.Button(
            self.button_frame, text="Save to CSV", command=self.save_to_csv
        )
        self.save_button.grid(row=0, column=4, padx=5, pady=5)

        self.browse_button = tk.Button(
            self.button_frame, text="Open Video File", command=self.browse_for_video
        )
        self.browse_button.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        skip_buttons_frame = tk.Frame(left_frame)
        skip_buttons_frame.pack()

        self.skip_backward_button = tk.Button(
            skip_buttons_frame,
            text="Skip Backward (seconds)",
            command=self.skip_backward,
        )
        self.skip_backward_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.seconds_entry = tk.Entry(skip_buttons_frame)
        self.seconds_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.skip_forward_button = tk.Button(
            skip_buttons_frame, text="Skip Forward (seconds)", command=self.skip_forward
        )
        self.skip_forward_button.pack(side=tk.LEFT, padx=5, pady=5)

        speed_buttons_frame = tk.Frame(left_frame)
        speed_buttons_frame.pack()

        self.speed_increase_button = tk.Button(
            speed_buttons_frame, text="Increase Speed", command=self.increase_speed
        )
        self.speed_increase_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add a label to display the current speed
        self.speed_label = tk.Label(
            speed_buttons_frame, text=f"Video Speed = {self.frame_skip}"
        )
        self.speed_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.speed_decrease_button = tk.Button(
            speed_buttons_frame, text="Decrease Speed", command=self.decrease_speed
        )
        self.speed_decrease_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Initially hide the standard buttons, seconds input, skip and speed buttons
        self.hide_standard_buttons()
        self.hide_seconds_input()

        # Right part (custom buttons, same dimensions)
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        for i, button_text in enumerate(self.buttons):
            custom_button = tk.Button(
                right_frame,
                text=button_text,
                command=lambda text=button_text: self.store_frame(text),
            )
            custom_button.pack(fill=tk.BOTH, expand=True)

    def hide_standard_buttons(self):
        self.play_button.grid_remove()
        self.prev_button.grid_remove()
        self.next_button.grid_remove()
        self.save_button.grid_remove()
        self.speed_decrease_button.pack_forget()
        self.speed_increase_button.pack_forget()
        self.speed_label.pack_forget()
        self.elapsed_time_label.grid_remove()

    def show_standard_buttons(self):
        self.play_button.grid()
        self.prev_button.grid()
        self.next_button.grid()
        self.save_button.grid()
        self.speed_decrease_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.speed_increase_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.speed_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.elapsed_time_label.grid()

    def hide_seconds_input(self):
        self.skip_backward_button.pack_forget()
        self.seconds_entry.pack_forget()
        self.skip_forward_button.pack_forget()

    def show_seconds_input(self):
        self.skip_backward_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.seconds_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.skip_forward_button.pack(side=tk.LEFT, padx=5, pady=5)

    def browse_for_video(self):
        video_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        if video_file:
            self.video_file = video_file
            self.cap = cv2.VideoCapture(video_file)
            self.frame_total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.frame_number = 0
            # Update the opened video name
            self.video_name_label.config(text=f"Video: {os.path.basename(video_file)}")
            # Hide the "Open Video File" button
            self.browse_button.grid_forget()
            # Show the standard buttons
            self.show_standard_buttons()
            # Show seconds input and skip buttons
            self.show_seconds_input()
            self.update_frame()

    def toggle_play(self):
        self.play = not self.play
        if self.play:
            self.play_button.config(text="Pause")
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.skip_backward_button.config(state=tk.DISABLED)
            self.skip_forward_button.config(state=tk.DISABLED)
            self.update_frame()
        else:
            self.play_button.config(text="Play")
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.skip_backward_button.config(state=tk.NORMAL)
            self.skip_forward_button.config(state=tk.NORMAL)

    def prev_frame(self):
        if self.frame_number > 0:
            self.frame_number -= 1
            self.update_frame()

    def next_frame(self):
        if self.frame_number < self.frame_total - 1:
            self.frame_number += 1
            self.update_frame()

    def skip_forward(self):
        seconds_to_skip = int(self.seconds_entry.get())
        frames_to_skip = int(seconds_to_skip * self.cap.get(cv2.CAP_PROP_FPS))
        new_frame_number = self.frame_number + frames_to_skip
        if new_frame_number < self.frame_total:
            self.frame_number = new_frame_number
            self.update_frame()

    def skip_backward(self):
        seconds_to_skip = int(self.seconds_entry.get())
        frames_to_skip = int(seconds_to_skip * self.cap.get(cv2.CAP_PROP_FPS))
        new_frame_number = self.frame_number - frames_to_skip
        if new_frame_number >= 0:
            self.frame_number = new_frame_number
            self.update_frame()

    def increase_speed(self):
        if self.frame_skip < 10:
            self.frame_skip += 1
            self.speed_label.config(text=f"Video Speed = {self.frame_skip}")

    def decrease_speed(self):
        if self.frame_skip > 1:
            self.frame_skip -= 1
            self.speed_label.config(text=f"Video Speed = {self.frame_skip}")

    def store_frame(self, button_text):
        self.button_states[button_text] = self.frame_number
        time_in_seconds = self.frame_number / self.cap.get(cv2.CAP_PROP_FPS)
        time_in_milliseconds = int(time_in_seconds * 1000)
        frame_data = {
            "Button": button_text,
            "Frame Number": self.frame_number,
            "Time (ms)": time_in_milliseconds,
        }
        self.frame_data_list.append(frame_data)
        print(
            f"Stored frame {self.frame_number} for button '{button_text}' at time {time_in_milliseconds} ms"
        )

    def save_to_csv(self):
        csv_file = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if csv_file:
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["Button", "Frame Number", "Time (ms)"]
                )
                writer.writeheader()
                writer.writerows(self.frame_data_list)

    def update_frame(self):
        if self.video_file and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (720, 480))
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                elapsed_time_seconds = self.frame_number / self.cap.get(
                    cv2.CAP_PROP_FPS
                )
                minutes = int(elapsed_time_seconds) // 60
                seconds = int(elapsed_time_seconds) % 60
                milliseconds = int(
                    (elapsed_time_seconds - int(elapsed_time_seconds)) * 1000
                )
                self.elapsed_time_label.config(
                    text=f"Elapsed Time: {minutes:02d}:{seconds:02d}:{milliseconds:03d}"
                )

                if self.play:
                    self.frame_number += self.frame_skip
                    if self.frame_number >= self.frame_total:
                        self.frame_number = 0
                    self.root.after(10, self.update_frame)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Annotate Video")
    root.geometry("1280x720")

    if os.path.exists("buttons.txt"):
        with open("buttons.txt", "r") as file:
            button_names = [name.strip() for name in file.read().split(",")]
        player = VideoPlayer(root, button_names)
        root.mainloop()
    else:
        print(
            "No 'buttons.txt' file found. Please create one with comma-separated button names."
        )
        button_names = []
