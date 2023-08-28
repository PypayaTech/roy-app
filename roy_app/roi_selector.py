import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ROISelector(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Default image size
        self.image_width = 800
        self.image_height = 600

        # Create a white image by default
        self.image = Image.new("RGB", (self.image_width, self.image_height), "white")

        # Frame for image
        self.image_frame = tk.Frame(self)
        self.image_frame.grid(row=0, column=0, sticky='nsew')

        # Frame for entries and button
        self.entry_frame = tk.Frame(self)
        self.entry_frame.grid(row=0, column=1, sticky='nsew')

        # Add a button for opening an image file
        open_button = tk.Button(self.entry_frame, text="Open Image", command=self.open_image)
        open_button.pack()

        # Create canvas
        self.canvas = tk.Canvas(self.image_frame, width=self.image_width, height=self.image_height)
        self.canvas.pack()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image_tk, anchor='nw')

        # Bounding box parameters
        self.box_x = tk.StringVar()
        self.box_y = tk.StringVar()
        self.box_width = tk.StringVar()
        self.box_height = tk.StringVar()

        self.box_x_norm = tk.StringVar()
        self.box_y_norm = tk.StringVar()
        self.box_width_norm = tk.StringVar()
        self.box_height_norm = tk.StringVar()

        # GUI widgets
        self.pixel_x_entry = self.create_entry("X (pixel): ", self.box_x, self.validate_pixel_value, self.entry_frame)
        self.pixel_y_entry = self.create_entry("Y (pixel): ", self.box_y, self.validate_pixel_value, self.entry_frame)
        self.pixel_width_entry = self.create_entry("Width (pixel): ", self.box_width, self.validate_pixel_value, self.entry_frame)
        self.pixel_height_entry = self.create_entry("Height (pixel): ", self.box_height, self.validate_pixel_value, self.entry_frame)

        self.norm_x_entry = self.create_entry("X (normalized): ", self.box_x_norm, self.validate_norm_value, self.entry_frame)
        self.norm_y_entry = self.create_entry("Y (normalized): ", self.box_y_norm, self.validate_norm_value, self.entry_frame)
        self.norm_width_entry = self.create_entry("Width (normalized): ", self.box_width_norm, self.validate_norm_value, self.entry_frame)
        self.norm_height_entry = self.create_entry("Height (normalized): ", self.box_height_norm,
                                                   self.validate_norm_value, self.entry_frame)

        # Initialize bounding box values
        self.box_x.set("100")
        self.box_y.set("100")
        self.box_width.set("100")
        self.box_height.set("100")

        self.update_normalized_values()

        # Mouse binding
        self.canvas.bind("<B1-Motion>", self.move_box)

        # Draw initial box
        self.draw_box()

        self.dragging = False

    def open_image(self):
        # Open the file dialog and get the path of the selected file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *jpeg")])

        # Check if a file was selected
        if file_path:
            # Load the image
            image = Image.open(file_path)

            # Update the image dimensions
            self.image_width = image.width
            self.image_height = image.height

            # Convert the image to a PhotoImage for use with tkinter
            self.photo_image = ImageTk.PhotoImage(image)

            # Update the canvas
            self.canvas.config(width=self.image_width, height=self.image_height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def drag_start(self, event):
        self.dragging = True

    def drag_end(self, event):
        self.dragging = False

    def create_entry(self, label, var, validation, frame):
        frame = tk.Frame(frame)
        frame.pack(fill=tk.X)
        tk.Label(frame, text=label).pack(side=tk.LEFT)
        vcmd = (self.register(validation), '%d', '%P')
        entry = tk.Entry(frame, textvariable=var, validate="key", validatecommand=vcmd)
        entry.pack(side=tk.LEFT)
        entry.bind("<Return>", self.entry_updated)
        return entry

    @staticmethod
    def validate_pixel_value(action, value):
        if action == '1':  # Insert
            if not value.isdigit():  # Check if the new text is an integer
                return False
        return True

    @staticmethod
    def validate_norm_value(action, value):
        if action == '1':  # Insert
            try:
                float_value = float(value)
                if float_value < 0.0 or float_value > 1.0:  # Check if the new value is between 0 and 1
                    return False
            except ValueError:  # The new text is not a float
                return False
        return True

    def entry_updated(self, event):
        # Check if dragging
        if self.dragging:
            return

        # Update pixel values from normalized values if necessary
        if event.widget in [self.norm_x_entry, self.norm_y_entry, self.norm_width_entry, self.norm_height_entry]:
            self.box_x.set(str(int(float(self.box_x_norm.get()) * self.image_width)))
            self.box_y.set(str(int(float(self.box_y_norm.get()) * self.image_height)))
            self.box_width.set(str(int(float(self.box_width_norm.get()) * self.image_width)))
            self.box_height.set(str(int(float(self.box_height_norm.get()) * self.image_height)))

        # Draw box with updated values
        self.draw_box()

        # Update normalized values from pixel values
        self.update_normalized_values()

    def draw_box(self):
        # Delete old box
        self.canvas.delete("box")

        # Draw new box
        x1 = int(float(self.box_x.get()))
        y1 = int(float(self.box_y.get()))
        x2 = x1 + int(float(self.box_width.get()))
        y2 = y1 + int(float(self.box_height.get()))
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", tags="box")

    def move_box(self, event):
        self.box_x.set(event.x - int(self.box_width.get()) / 2)
        self.box_y.set(event.y - int(self.box_height.get()) / 2)

        # Draw box with updated values
        self.draw_box()

        # Update normalized values from pixel values
        self.update_normalized_values()

    def update_normalized_values(self):
        self.box_x_norm.set(format(float(self.box_x.get()) / self.image_width, '.4f'))
        self.box_y_norm.set(format(float(self.box_y.get()) / self.image_height, '.4f'))
        self.box_width_norm.set(format(float(self.box_width.get()) / self.image_width, '.4f'))
        self.box_height_norm.set(format(float(self.box_height.get()) / self.image_height, '.4f'))
