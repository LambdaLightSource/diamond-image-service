import os

import numpy
from PIL import Image

IMAGES_TO_GENERATE = 1000
IMAGE_DIR = "generated_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

for i in range(IMAGES_TO_GENERATE):
    imarray = numpy.random.rand(250, 250, 3) * 255
    im = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
    im.save(f"{IMAGE_DIR}/random_image_{str(i).zfill(6)}.png")

print("Image generation complete")
