from PIL import Image, ImageDraw
from pathlib import Path

IMAGES_FOLDER = Path('images')

# The available ASCII characters that can be used to create the ASCII art
ASCII_CHARS = ['@', '#', '%', 'S', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS_LENGTH = len(ASCII_CHARS)
ONE_CHAR_WIDTH = 6
ONE_CHAR_HEIGHT = 15


def resize_image(image: Image, new_width=100) -> Image:
    """
    This method resizes the image such that the ascii art will have approximately the same aspect ratio as the original image.
    The new image will have N amount of pixels horizontally, with N equals the given new_width.
    This method returns the resized image, the width of this resized image and the height of this resized image.
    """
    width, height = image.size
    ratio = height / width
    resize_factor = calculate_resize_factor(new_width)
    new_height = int(new_width * ratio * (ONE_CHAR_WIDTH / ONE_CHAR_HEIGHT) * resize_factor)
    resized_image = image.resize((new_width, new_height))
    return resized_image, new_width, new_height


def calculate_resize_factor(new_width: int) -> float:
    """
    This method returns a resize factor depending on the new_width.
    This resize factor is used in the resize_image() method.
    """
    if new_width < 100:
        return 1.0666666666666667
    elif new_width > 750:
        return 0.95
    else:
        point_one = (100, 1.0666666666666667)
        point_two = (750, 0.95)
        slope = (point_one[1] - point_two[1]) / (point_one[0] - point_two[0])
        resize_factor = point_one[1] + slope*(new_width - point_one[0])
        return resize_factor


def convert_image_to_gray_scale(image: Image) -> Image:
    """
    This method creates the gray scale image from the given image and returns this gray scale image.
    """
    return image.convert('L')


def convert_grayscale_image_to_ascii_string(grayscale_image: Image) -> str:
    """
    Each pixel in the given grayscale_image will be mapped to an ascii character depending on its grayscale value.
    This method will return the string made from all these characters.
    """
    result = ''
    width, height = grayscale_image.size
    grayscale_pixels = grayscale_image.load()

    for y in range(height):
        for x in range(width):
            current_pixel_grayscale_value = grayscale_pixels[x, y]
            ascii_char = ASCII_CHARS[current_pixel_grayscale_value // (int(255 / ASCII_CHARS_LENGTH) + 1)]
            result += ascii_char
        result += '\n'

    return result


def write_ascii_string_to_file(file_name: str, ascii_string: str) -> None:
    """
    This method writes the given ascii_string to the file with the given file_name.
    """
    with open(file_name, 'w') as output_file:
        output_file.write(ascii_string)


def save_ascii_string_as_image(file_name: Path, ascii_string: str) -> None:
    """
    This method creates an image and draws the characters given in the ascii_string on this image.
    The file name will be the given file_name.
    """
    ascii_char_list = ascii_string.split("\n")[:-1]  # [:-1] removes last element from list which should just be ''
    width = len(ascii_char_list[0])
    height = len(ascii_char_list)
    output_image = Image.new('L', (ONE_CHAR_WIDTH * width, ONE_CHAR_HEIGHT * height), color=255)
    drawable_image = ImageDraw.Draw(output_image)
    drawable_image.text((0, 0), ascii_string, fill=0)
    # check if the subdirectory exists and if it does not then make it
    subdirectory_path = file_name.parent
    if not subdirectory_path.is_dir():
        subdirectory_path.mkdir()
    output_image.save(file_name)


def create_ascii_art(input_image_file_name: str, resize_width: int) -> None:
    """
    This method creates ascii_art of the given image and saves this new image.
    The image will have N ascii characters on each row of the image, with N equals the given resize_width.
    """
    with Image.open(IMAGES_FOLDER / input_image_file_name) as image:
        resized_image, width, height = resize_image(image, resize_width)
    # get the gray scale image
    grayscale_image = convert_image_to_gray_scale(resized_image)
    # generate the ascii string
    ascii_string = convert_grayscale_image_to_ascii_string(grayscale_image)
    # create the output file name
    input_file_base_name = input_image_file_name.split('.')[0]
    output_image_file_name = IMAGES_FOLDER / (input_file_base_name + '_OUT') / (input_file_base_name + f'_{width}x{height}' + '_ascii.png')
    # generate and save the ascii image
    save_ascii_string_as_image(output_image_file_name, ascii_string)


if __name__ == '__main__':
    create_ascii_art('Kanagawa.jpg', 3000)
