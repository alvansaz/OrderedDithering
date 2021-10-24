from PIL import Image
import numpy as np


def build_dither_matrix(n):
    if n == 2:
        return np.array([
            [0, 2],
            [3, 1]
        ])
    else:
        return np.block([
            [build_dither_matrix(n / 2) * 4,
             build_dither_matrix(n / 2) * 4 + 2],
            [build_dither_matrix(n / 2) * 4 + 3,
             build_dither_matrix(n / 2) * 4 + 1]
        ])


def ordered_dithering(gray_image, n, output_name):
    gi = gray_image
    dither_matrix = build_dither_matrix(n)

    for i in range(gi.size[0]):
        for j in range(gi.size[1]):
            if gi.getpixel((i, j)) / (256 / (n * n)) > dither_matrix[i % n, j % n]:
                gi.putpixel((i, j),  255)
            else:
                gi.putpixel((i, j), 0)

    try:
        gi.save("../outputs/" + output_name)
        return 0
    except ValueError as ve:
        print("\nPlease add the file format (like '.png') at the end of output file name")
        return 1


if __name__ == '__main__':

    image_path = input(
        "\n\nEnter the path of the image (e.g. '../images/lana.png') : ")
    n = int(input("\nEnter the dither matrix dimension (e.g. 2, 4, 8, etc.) : "))
    output_name = input(
        "\nEnter the name of your output file (e.g. 'lanaoutput.png') : ")

    original_image = Image.open(image_path)

    greyscale_image = original_image.convert('L')

    if ordered_dithering(greyscale_image, n, output_name) == 0:
        print("\n===> Done! <===\n")
    else:
        print("\n===> Not completed! Try again <===\n")
