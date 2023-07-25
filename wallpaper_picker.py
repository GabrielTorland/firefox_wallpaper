import os
import random
import re
from PIL import Image
import argparse
from __update_db import update

def parse_arguments():
    """
    Parse and return command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Choose a specific image or a random one from the directory.')
    parser.add_argument('--name', type=str, help='The name of the image to be chosen')
    return parser.parse_args()

def get_image_filepaths(dirpath):
    """
    Get a list of image file paths from the directory.

    Args:
        dirpath (str): The directory path.

    Returns:
        list: List of image file paths.
    """
    image_filepaths = []
    filenames = os.listdir(dirpath)
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        try:
            Image.open(filepath)
            image_filepaths.append(filepath)
        except IOError:
            pass  # Not an image file
    return image_filepaths

def choose_image(image_filepaths, image_name=None):
    """
    Choose an image either randomly or by a specific name.

    Args:
        image_filepaths (list): List of image file paths.
        image_name (str, optional): The name of the image to be chosen. Defaults to None.

    Returns:
        str: Chosen image file path.
    """
    if image_name:
        chosen_image = next((img for img in image_filepaths if image_name in img), None)
        if not chosen_image:
            raise Exception(f'Image with name {image_name} not found in the directory.')
    else:
        chosen_image = random.choice(image_filepaths)
    return chosen_image

def replace_image_url_in_css(css_path, image_path):
    """
    Replace the image URL in the CSS file.

    Args:
        css_path (str): The path to the CSS file.
        image_path (str): The path to the chosen image.
    """
    relative_path = os.path.relpath(image_path, os.path.dirname(css_path))
    with open(css_path, 'r') as f:
        css = f.read()
    new_css = re.sub(r'url\(imgs/.*\)', f'url({relative_path})', css)
    with open(css_path, 'w') as f:
        f.write(new_css)
    print(f'Replaced image URL with "{relative_path}"')

def main():
    """
    Main function of the script.
    """

    print("Updating image database...")
    update()
    print("Update complete.")

    args = parse_arguments()

    dirpath = 'imgs/'
    image_filepaths = get_image_filepaths(dirpath)

    if len(image_filepaths) == 0:
        raise Exception('No image files found in the directory.')

    chosen_image = choose_image(image_filepaths, args.name)

    css_path = 'wallpaper.css'
    replace_image_url_in_css(css_path, chosen_image)

if __name__ == "__main__":
    main()

