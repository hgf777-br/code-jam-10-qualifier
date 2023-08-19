import cv2 as cv
from cv2 import IMREAD_UNCHANGED
import numpy as np

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    valid_tiles = image_size[0] % tile_size[0] == 0 and image_size[1] % tile_size[1] == 0 # Check if the tile size must divide each image dimension without remainders
    ordering_size = (image_size[0] // tile_size[0]) * (image_size[1] // tile_size[1]) # Calculate the number of tiles in the image
    valid_ordering = len(ordering) == len(set(ordering)) and len(ordering) == ordering_size # Check if `ordering` must use each input tile exactly once.

    return valid_tiles and valid_ordering


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    with open(image_path, 'r') as f:
        image = cv.imread(image_path, IMREAD_UNCHANGED) # reading scrambled image from disk
        image_size = image.shape[:-1] # calculating image size
        final_image = np.zeros_like(image) # creating array to receive the final image

        if valid_input(image_size, tile_size, ordering): # checking if the input is valid
            fy = image_size[0] // tile_size[0] # calculating number of vertical tiles
            fx = image_size[1] // tile_size[1] # calculating number of horizontal tiles
            no = np.array(ordering).reshape(fy,fx) # creating an array for ordering with the same image tile dimension
            for y in range(fy): # Looping in all rows
                for x in range(fx): # Looping in all columns
                    yo = (no[y,x] // fx) * tile_size[0] # Original tile vertival coordinate
                    xo = (no[y,x] % fx) * tile_size[1] # Original tile horizontal coordinate
                    yf = y * tile_size[0] # Final tile vertival coordinate
                    xf = x * tile_size[1] # Final tile horizontal coordinate
                    tile = image[yo:yo+tile_size[0], xo:xo+tile_size[1]] # Get original tile
                    final_image[yf:yf+tile_size[0], xf:xf+tile_size[1]] = tile # Copy original tile to the final image
            cv.imwrite(out_path, final_image) # Write the unscrambled image to disk
        else:
            raise ValueError('The tile size or ordering are not valid for the given image') # Raise error if the input is not valid
