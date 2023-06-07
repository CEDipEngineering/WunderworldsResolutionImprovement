import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from PdfManipulator import PdfManipulator
from ImageImprover import ImageImprover
from random import randint
import sys


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")

        # Initialize variables for brightness and contrast
        self.brightness = 1.0
        self.contrast = 1.0

        # Create a label to display the original image
        self.original_image_label = tk.Label(root)
        self.original_image_label.pack(side=tk.LEFT, padx=10)

        # Create a label to display the adjusted image
        self.adjusted_image_label = tk.Label(root)
        self.adjusted_image_label.pack(side=tk.LEFT, padx=10)

        # Create sliders for brightness and contrast
        self.brightness_slider = tk.Scale(
            root,
            label="Brightness",
            from_=0.0,
            to=2.0,
            resolution=0.01,
            command=self.update_image
        )
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(
            root,
            label="Contrast",
            from_=0.0,
            to=2.0,
            resolution=0.01,
            command=self.update_image
        )
        self.contrast_slider.pack()

        # Create a button to select an image file
        self.select_image_button = tk.Button(
            root,
            text="Select Pdf",
            command=self.select_image
        )
        self.select_image_button.pack(pady=10)

        # Set the initial image paths
        self.original_image = None
        self.adjusted_image = None

        self.II = ImageImprover()

        # Update the image display
        self.update_image()

    def select_image(self):
        # Open a file dialog to select an image file
        filetypes = (("PDF file", "*.pdf"), ("All Files", "*.*"))
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        print("Selected file: {}".format(filepath))
        
        if filepath:
            # Extractor
            PM = PdfManipulator(filepath)
            images = PM.get_cards()       

            # Set original image
            self.original_image = images[0]

            # Update the adjusted image path
            self.adjusted_image = self.II.improve(images[0])

            # Update the image display
            self.update_image()

    def update_image(self, *args):
        if self.original_image is None: return

        # Update the brightness and contrast variables
        self.brightness = self.brightness_slider.get()
        self.contrast = self.contrast_slider.get()

        # Apply brightness and contrast adjustments to the original image
        self.adjusted_image = self.II.improve(self.original_image)
        
        # Convert the adjusted image to a format that Tkinter can display
        self.adjusted_image_tk = ImageTk.PhotoImage(self.adjusted_image)
        self.original_image_tk = ImageTk.PhotoImage(self.original_image)

        # Update the image labels
        self.adjusted_image_label.configure(image = self.adjusted_image_tk)
        self.original_image_label.configure(image = self.original_image_tk)

# Create the root window
root = tk.Tk()

# Create an instance of the SimpleGUI class
gui = SimpleGUI(root)

# Start the Tkinter event loop
root.mainloop()
