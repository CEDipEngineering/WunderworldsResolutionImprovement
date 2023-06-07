from typing import List
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from PIL.PpmImagePlugin import PpmImageFile

class ImageImprover:

    def __init__(self) -> None:
        pass

    def improve(self, image: PpmImageFile, sharpness_factor=5.0, cutoff=1.0, color_factor=1.0, contrast_factor=1.0) -> PpmImageFile:
        """
        Method applied to images, meant to improve contrast and readability.
        """
        image = self._color(image, color_factor)

        image = self._contrast(image, contrast_factor)
        
        image = self._autocontrast(image, cutoff)

        image = self._sharpen(image, sharpness_factor)
        return image

    def improve_all(self, images: List[PpmImageFile], sharpness_factor=5.0, cutoff=1.0, color_factor=1.0, contrast_factor=1.0) -> List[PpmImageFile]:
        """
        Wrapper to call improve method on every image on a list, and return a new list with results.
        """
        return [self.improve(im, sharpness_factor, cutoff, color_factor, contrast_factor) for im in images]

    def _color(self, image: PpmImageFile, factor) -> PpmImageFile:
        enhancer = ImageEnhance.Sharpness(image)    
        return enhancer.enhance(factor)

    def _contrast(self, image: PpmImageFile, factor) -> PpmImageFile:
        enhancer = ImageEnhance.Sharpness(image)    
        return enhancer.enhance(factor)

    def _sharpen(self, image: PpmImageFile, factor) -> PpmImageFile:
        enhancer = ImageEnhance.Sharpness(image)    
        return enhancer.enhance(factor)

    def _autocontrast(self, image: PpmImageFile, cutoff) -> PpmImageFile:
        return ImageOps.autocontrast(image, cutoff)
    
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