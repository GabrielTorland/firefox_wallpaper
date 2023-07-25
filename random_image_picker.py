import os
import random
import re
from PIL import Image

# Initialize an empty list for image file paths
image_filepaths = []

# Define the path to your CSS file
css_path = 'wallpaper.css'

# Walk the 'img' directory
for dirpath, dirnames, filenames in os.walk('img/'):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        try:
            # Try to open the file with PIL
            Image.open(filepath)
            # If it can be opened as an image, append it to the list
            image_filepaths.append(filepath)
        except IOError:
            pass  # Not an image file

# If no image files found, raise an exception
if not image_filepaths:
    raise Exception('No image files found in the directory.')

# Randomly choose one
chosen_image = random.choice(image_filepaths)

# Make the chosen image path relative to the CSS file
relative_path = os.path.relpath(chosen_image, os.path.dirname(css_path))

# Read the original CSS file
with open(css_path, 'r') as f:
    css = f.read()

# Replace the URL using regex
new_css = re.sub(r'url\(img/(.*?)\)', f'url("{relative_path}")', css)

# Write the modified CSS back to the file
with open(css_path, 'w') as f:
    f.write(new_css)

print(f'Replaced image URL with "{relative_path}"')

