
from typing import List
from PIL import Image
from pdf2image import convert_from_path
import img2pdf
import os

class PdfManipulator:

    # Vertical pixel values for card starts and ends
    VERTICAL_CUTS = [
        [23, 532],
        [555, 1063],
        [1086, 1595]
    ]

    # Horizontal pixel values for card starts and ends
    HORIZONTAL_CUTS = [
        [23, 732],
        [747, 1456],
        [1494, 2202]
    ]

    # Silly heuristic to identify blank card slots faster
    # If pixel is (255, 255, 255) in all these pixels, image is considered blank
    SAMPLE_COORDINATES = [
        (180, 199),
        (170, 200),
        (175, 202),
        (178, 199),
        (182, 199),
        (181, 205),
        (380, 159),
        (370, 250),
        (375, 252),
        (378, 159),
        (382, 159),
        (381, 255),
    ]

    def __init__(self, pdf_path: str) -> None:
        self.pdf_pages = convert_from_path(pdf_path, fmt="tiff")
        self._cut_all_cards()

    def is_all_white(self, image: Image.Image) -> bool:
        """
        Function used to identify if current card image crop is all white.
        Instead of checking some kind of sum, I decided to use a silly heuristic.
        I check a few random spots in the card sprite to see if they're all white.
        The odds that a valid card will have white on all these is astronomically low, so it's fine.
        Don't ask me why I did it like this.
        """
        white = 0
        for pos in PdfManipulator.SAMPLE_COORDINATES:
            if image.getpixel(pos) == (255, 255, 255):
                white += 1
        return white == len(PdfManipulator.SAMPLE_COORDINATES)

    def get_pixel_box(self, page_index: int, card_index: int) -> List[int]:
        # Identify position in grid
        row     = card_index//3
        column  = card_index%3
        
        # Identify pixel coordinates
        left    = PdfManipulator.VERTICAL_CUTS[column][0]
        upper   = PdfManipulator.HORIZONTAL_CUTS[row][0]
        right   = PdfManipulator.VERTICAL_CUTS[column][1]
        bottom  = PdfManipulator.HORIZONTAL_CUTS[row][1]

        return [left, upper, right, bottom]

    def _get_card_image(self, page_index: int, card_index: int):
        """
        Function used to cut out the cards from the full page ppm image.
        I hand measured the pixel offsets for each column and row, then do some basic maths.
        """
        return self.pdf_pages[page_index].crop(self.get_pixel_box(page_index, card_index))

    def _cut_all_cards(self) -> List[Image.Image]:
        """
        Function called on init, responsible for looping over all pages of the supplied pdf and extracting all cards.
        """
        # Store cards in attribute list
        self.card_list = []

        # For every page in the pdf
        for page_index in range(len(self.pdf_pages)):
            # There can only be 9 cards per page
            for card_index in range(9):
                # Cut out card
                img = self._get_card_image(page_index, card_index)
                # If it's white don't keep it.
                if self.is_all_white(img):
                    continue
                self.card_list.append(img)
    
    def get_cards(self):
        """
        Simple getter for cards. Essentially, you should only need to construct an ImageExtractor, then call this.
        """
        return self.card_list

    def dump_changes(self, path: str, improved_images) -> None:
        """
        Function used to write improvements to new pdf.
        After making all changes, take list of improved card images and
        overwrite the previous cards in the pdf original images.
        This means that the dimensions of the pdf should not change.
        """
        
        # Use paste function from PIL to place new cards over old ones
        for index, card in enumerate(improved_images):
            page_index = index//9 # 9 cards per page
            card_index = index%9 # Card position in page
            box = self.get_pixel_box(page_index, card_index)
            self.pdf_pages[page_index].paste(card, box=box)

        # Save each page to a temporary file in tmp dir
        n = 0
        names = []
        for page in self.pdf_pages:
            name = "tmp/{}_tmp.tiff".format(n)
            names.append(name)
            page.save(name)
            n+=1

        # Use img2pdf to write to a new pdf
        with open(path, 'wb') as f:
            f.write(img2pdf.convert(names))

        # Delete tmp files
        self._cleanup()
        
    def _cleanup(self):
        """
        Internal method to delete all tmp files.
        """
        # Iterate over all files in the folder
        for filename in os.listdir("tmp"):
            file_path = os.path.join("tmp", filename)
            
            # Check if the path is a file (not a folder)
            if os.path.isfile(file_path) and file_path != ".gitkeep":
                try:
                    # Delete the file
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting rmp file: {file_path} - {e}")







