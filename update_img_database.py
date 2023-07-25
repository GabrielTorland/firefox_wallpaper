import os
import json
import hashlib
import shutil
from pathlib import Path
from PIL import Image

IMG_DIR = Path('img')
DB_FILE = Path('image_db.json')

# Load the existing database
try:
    with open(DB_FILE, 'r') as f:
        db = json.load(f)
except FileNotFoundError:
    db = []

# Go through all files in the directory, recursively
for filepath in IMG_DIR.rglob('*'):
    if filepath.is_file():
        # Attempt to open the file as an image
        try:
            Image.open(filepath)
        except IOError:
            # If it's not an image file, remove it
            filepath.unlink()
            continue

        # Generate a unique name using the SHA-256 hash of the file's relative path
        unique_name = hashlib.sha256(str(filepath).encode()).hexdigest() + filepath.suffix

        # If the file isn't in the database, rename it and add it to the database
        if unique_name not in db:
            shutil.move(filepath, IMG_DIR / unique_name)
            db.append(unique_name)

# Go through all directories in reverse order and remove any that are empty
for filepath in sorted(IMG_DIR.rglob('*'), reverse=True):
    if filepath.is_dir() and not any(filepath.iterdir()):
        filepath.rmdir()

# Go through all files in the database and remove any that don't exist anymore
for filename in db.copy():  # Iterate over a copy of the list so we can remove items while iterating
    if not (IMG_DIR / filename).is_file():
        db.remove(filename)

# Save the updated database
with open(DB_FILE, 'w') as f:
    json.dump(db, f)
