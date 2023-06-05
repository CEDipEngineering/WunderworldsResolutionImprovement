from typing import List
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from PIL.PpmImagePlugin import PpmImageFile

class ImageImprover:

    def __init__(self) -> None:
        self.sharpness_factor   = 5.0

    def improve(self, image: PpmImageFile) -> PpmImageFile:
        """
        Method applied to images, meant to improve contrast and readability.
        """
        image = self._contrast(image)
        image = self._sharpen(image)
        return image

    def improve_all(self, images: List[PpmImageFile]) -> List[PpmImageFile]:
        """
        Wrapper to call improve method on every image on a list, and return a new list with results.
        """
        return [self.improve(im) for im in images]

    def _sharpen(self, image: PpmImageFile) -> PpmImageFile:
        enhancer = ImageEnhance.Sharpness(image)    
        return enhancer.enhance(self.sharpness_factor)

    def _contrast(self, image: PpmImageFile) -> PpmImageFile:
        return ImageOps.autocontrast(image)
    
    def _save_image(self, image: Image.Image, out_path: str) -> None:
        image.save(out_path)

    def _compare_debug(self, image: PpmImageFile) -> None:
        """
        Debug method, used to draw both original and transformed images side by side.
        """
        # Create a copy then make improvements
        orig = image.copy()
        improved = self.improve(image)

        # New image, used to draw them side-by-side
        new_image = Image.new('RGB', (orig.size[0]*2, orig.size[1]))

        # Paste the images side by side
        new_image.paste(orig, (0, 0))
        new_image.paste(improved, (orig.size[0], 0))

        # Display the new image
        new_image.show()