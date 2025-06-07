from PIL import Image
import numpy as np

img = Image.open("funny.jpg")
greyscale = img.convert("L")
org_matrix = np.array(greyscale)

print(org_matrix)