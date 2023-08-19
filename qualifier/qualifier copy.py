import cv2 as cv
import numpy as np

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    valid_tiles = image_size[0] % tile_size[0] == 0 and image_size[1] % tile_size[1] == 0
    ordering_size = (image_size[0] // tile_size[0]) * (image_size[1] // tile_size[1])
    valid_ordering = len(ordering) == len(set(ordering)) and len(ordering) == ordering_size

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
        image = cv.imread(image_path)
        image_size = image.shape[:-1]
        final_image = np.zeros_like(image)
        if valid_input(image_size, tile_size, ordering):
            fx = image_size[0] // tile_size[0]
            fy = image_size[1] // tile_size[1]
            no = np.array(ordering).reshape(fx,fy)
            for x in range(fx):
                for y in range(fy):
                    xo = (no[x,y] // fy) * tile_size[0]
                    yo = (no[x,y] % fy) * tile_size[1]
                    xf = x * tile_size[0]
                    yf = y * tile_size[0]
                    tile = image[xo:xo+tile_size[0], yo:yo+tile_size[1]]
                    final_image[xf:xf+tile_size[0], yf:yf+tile_size[1]] = tile
            cv.imwrite(out_path, final_image);
        else:
            raise ValueError('The tile size or ordering are not valid for the given image')


ordering = []
ordering_path = r'qualifier/images/pydis_logo_order.txt'
with open(ordering_path, 'r') as f:
    ordering = [int(x) for x in f.read().strip().splitlines()]
image_path = r'qualifier/images/pydis_logo_scrambled.png'
output_path = r'qualifier/images/hgf1.png'
tile = (256, 256)
rearrange_tiles(image_path, tile, ordering, output_path)
ordering_path = r'qualifier/images/great_wave_order.txt'
with open(ordering_path, 'r') as f:
        ordering = [int(x) for x in f.read().strip().splitlines()]
image_path = r'qualifier/images/great_wave_scrambled.png'
output_path = r'qualifier/images/hgf2.png'
tile = (16, 16)
rearrange_tiles(image_path, tile, ordering, output_path)
ordering_path = r'qualifier/images/secret_image1_order.txt'
with open(ordering_path, 'r') as f:
        ordering = [int(x) for x in f.read().strip().splitlines()]
image_path = r'qualifier/images/secret_image1_scrambled.png'
output_path = r'qualifier/images/hgf3.png'
tile = (20, 20)
rearrange_tiles(image_path, tile, ordering, output_path)
ordering_path = r'qualifier/images/secret_image2_order.txt'
with open(ordering_path, 'r') as f:
        ordering = [int(x) for x in f.read().strip().splitlines()]
image_path = r'qualifier/images/secret_image2_scrambled.png'
output_path = r'qualifier/images/hgf4.png'
tile = (20, 20)
rearrange_tiles(image_path, tile, ordering, output_path)