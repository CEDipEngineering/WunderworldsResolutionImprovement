import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from PdfManipulator import PdfManipulator
from ImageImprover import ImageImprover
from random import choice
import sys


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")

        self.image_frame = tk.Frame(root)
        self.image_frame.pack(side=tk.TOP, pady=20)


        # Create a label to display the original image
        self.original_frame = tk.Frame(self.image_frame)
        self.original_frame.pack(side=tk.LEFT, padx=10)

        self.original_text_label = tk.Label(self.original_frame, text = "Original Image:")
        self.original_text_label.pack(side=tk.TOP, anchor=tk.CENTER)
        
        self.original_image_label = tk.Label(self.original_frame)
        self.original_image_label.pack(side=tk.BOTTOM)


        # Create a label to display the adjusted image
        self.adjusted_frame = tk.Frame(self.image_frame)
        self.adjusted_frame.pack(side=tk.RIGHT, padx=10)
        
        self.adjusted_text_label = tk.Label(self.adjusted_frame, text = "Adjusted Image:")
        self.adjusted_text_label.pack(side=tk.TOP, anchor=tk.CENTER)
        
        self.adjusted_image_label = tk.Label(self.adjusted_frame)
        self.adjusted_image_label.pack(side=tk.BOTTOM, padx=10)

        # Sliders

        self.sliders_frame = tk.Frame(root)
        self.sliders_frame.pack(side=tk.BOTTOM)

        self.sharpness_frame = tk.Frame(self.sliders_frame)
        self.sharpness_frame.pack(side=tk.LEFT)
        self.sharpness_label = tk.Label(self.sharpness_frame, text="Sharpness")
        self.sharpness_label.pack(padx=10)
        self.sharpness_slider = tk.Scale(
            self.sharpness_frame,
            from_=0.0,
            to=10.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.update_image
        )
        self.sharpness_slider.pack(side=tk.LEFT)
        self.sharpness_slider.set(1.0)

        self.cutoff_frame = tk.Frame(self.sliders_frame)
        self.cutoff_frame.pack(side=tk.LEFT)
        self.cutoff_label = tk.Label(self.cutoff_frame, text="Contrast Cutoff")
        self.cutoff_label.pack(padx=10)
        self.cutoff_slider = tk.Scale(
            self.cutoff_frame,
            from_=0.0,
            to=2.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.update_image
        )
        self.cutoff_slider.pack(side=tk.LEFT)
        self.cutoff_slider.set(1.0)

        self.color_frame = tk.Frame(self.sliders_frame)
        self.color_frame.pack(side=tk.LEFT)
        self.color_label = tk.Label(self.color_frame, text="Color")
        self.color_label.pack(padx=10)
        self.color_slider = tk.Scale(
            self.color_frame,
            from_=0.0,
            to=2.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.update_image
        )
        self.color_slider.pack(side=tk.LEFT)
        self.color_slider.set(1.0)

        self.contrast_frame = tk.Frame(self.sliders_frame)
        self.contrast_frame.pack(side=tk.LEFT)
        self.contrast_label = tk.Label(self.contrast_frame, text="Contrast")
        self.contrast_label.pack(padx=10)
        self.contrast_slider = tk.Scale(
            self.contrast_frame,
            from_=0.0,
            to=2.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.update_image
        )
        self.contrast_slider.pack(side=tk.LEFT)
        self.contrast_slider.set(1.0)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10, anchor=tk.CENTER)

        # Create a button to select an image file
        self.select_file_button = tk.Button(
            self.button_frame,
            text="Select Pdf",
            command=self.select_pdf
        )
        self.select_file_button.pack(side=tk.LEFT)

        # Create a button to select an image file
        self.export_button = tk.Button(
            self.button_frame,
            text="Save result",
            command=self.export_all
        )
        self.export_button.pack(side=tk.LEFT)

        self.cycle_image_button = tk.Button(
            self.button_frame,
            text="Change Preview Image",
            command=self.cycle_image
        )
        self.cycle_image_button.pack(side=tk.LEFT)

        # Set the initial image paths
        self.original_image = None
        self.adjusted_image = None

        self.II = ImageImprover()

        # Update the image display
        self.update_image()

    def cycle_image(self):
        if self.original_image is None: return
        self.original_image = choice(self.PM.get_cards())
        self.update_image()

    def select_pdf(self):
        # Open a file dialog to select an image file
        filetypes = (("PDF file", "*.pdf"), ("All Files", "*.*"))
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        print("Selected file: {}".format(filepath))
        
        if filepath:
            # Extractor
            self.PM = PdfManipulator(filepath)
            images = self.PM.get_cards()
            print("Found pdf with {} cards!".format(len(images)))     

            # Set original image
            self.original_image = images[0]

            # Update the image display
            self.update_image()

    def update_image(self, *args):
        if self.original_image is None: return

        # Apply brightness and contrast adjustments to the original image
        self.adjusted_image = self.II.improve(
            self.original_image,
            self.sharpness_slider.get(),
            self.cutoff_slider.get(),
            self.color_slider.get(),
            self.contrast_slider.get()
        )
        
        # Convert the adjusted image to a format that Tkinter can display
        self.adjusted_image_tk = ImageTk.PhotoImage(self.adjusted_image)
        self.original_image_tk = ImageTk.PhotoImage(self.original_image)

        # Update the image labels
        self.adjusted_image_label.configure(image = self.adjusted_image_tk)
        self.original_image_label.configure(image = self.original_image_tk)

    def export_all(self):
        print("Exporting {} cards using settings:\nSharpness: {}\nCutoff: {}\nColor: {}\nContrast: {}".format(
            len(self.PM.get_cards()),             
            self.sharpness_slider.get(),
            self.cutoff_slider.get(),
            self.color_slider.get(),
            self.contrast_slider.get()
            )
        )
        improved_images = self.II.improve_all(
            self.PM.get_cards(),
            self.sharpness_slider.get(),
            self.cutoff_slider.get(),
            self.color_slider.get(),
            self.contrast_slider.get()
        )

        path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="output.pdf")
        self.PM.dump_changes(path, improved_images)
        print("Export Done!")

# Create the root window
root = tk.Tk()

# Create an instance of the SimpleGUI class
gui = SimpleGUI(root)

# Start the Tkinter event loop
root.mainloop()
