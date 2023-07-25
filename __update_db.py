import os
import json
import hashlib
import shutil
from pathlib import Path
from PIL import Image

IMG_DIR = Path('imgs')
DB_FILE = Path('image_db.json')

def load_image_database(db_file):
    """
    Load the existing image database, or create a new one if it doesn't exist.

    Args:
        db_file (Path): The database file path.

    Returns:
        list: The image database.
    """
    try:
        with open(db_file, 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = []
    return db

def cleanup_and_hash_images(img_dir, db):
    """
    Go through all files in the directory, attempt to open them as images, remove any non-image files,
    and rename and add any new image files to the database.

    Args:
        img_dir (Path): The image directory path.
        db (list): The image database.
    """
    for filepath in img_dir.rglob('*'):
        if filepath.is_file():
            try:
                Image.open(filepath)
            except IOError:
                filepath.unlink()
                continue

            source = str(filepath)
            file_name = source.split("/")[-1]
            if file_name not in db:
                unique_name = hashlib.sha256(str(filepath).encode()).hexdigest() + filepath.suffix
                shutil.move(filepath, img_dir / unique_name)
                db.append(unique_name)
            else:
                db.append(file_name)

def remove_empty_dirs(img_dir):
    """
    Go through all directories in reverse order and remove any that are empty.

    Args:
        img_dir (Path): The image directory path.
    """
    for filepath in sorted(img_dir.rglob('*'), reverse=True):
        if filepath.is_dir() and not any(filepath.iterdir()):
            filepath.rmdir()

def remove_nonexistent_files(img_dir, db):
    """
    Go through all files in the database and remove any that don't exist anymore.

    Args:
        img_dir (Path): The image directory path.
        db (list): The image database.
    """
    for filename in db.copy():  # Iterate over a copy of the list so we can remove items while iterating
        if not (img_dir / filename).is_file():
            db.remove(filename)

def save_image_database(db_file, db):
    """
    Save the updated image database.

    Args:
        db_file (Path): The database file path.
        db (list): The image database.
    """
    with open(db_file, 'w') as f:
        json.dump(db, f)

def update():
    """
    Update the image database. This involves changing filename on all the images.
    """
    db = load_image_database(DB_FILE)
    cleanup_and_hash_images(IMG_DIR, db)
    remove_empty_dirs(IMG_DIR)
    remove_nonexistent_files(IMG_DIR, db)
    save_image_database(DB_FILE, db)

if __name__ == "__main__":
    update()
