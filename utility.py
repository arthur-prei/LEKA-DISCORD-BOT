# utility module
from PIL import Image
import json
import io
import os

# GENERATE THE PHOTO THAT IS USED ON THE SHIP_MEMBERS FUNCTION ON entertainment.py

def create_image(image, emoji: None, image2, base_height, padding_px):

    padding = padding_px

    def resize_image(img, height):
        proportion = height / img.height
        width = int(img.width * proportion)
        return img.resize((width, height))
    
    left_image = Image.open(fp=image).convert("RGBA")
    right_image = Image.open(fp=image2).convert("RGBA")

    left_image = resize_image(left_image, base_height)
    right_image = resize_image(right_image, base_height)
    
    x = padding
    
    if emoji:
        middle_image = Image.open(fp=emoji).convert("RGBA")
        middle_image = resize_image(middle_image, int(base_height * 0.4))
        total_width = left_image.width + middle_image.width + right_image.width + padding*4
    else:
        total_width = left_image.width + right_image.width + padding*3

    final_image = Image.new("RGBA", (total_width, base_height))

    # First image
    final_image.paste(left_image, (x, 0))
    x += left_image.width + padding

    # Emoji
    if emoji:
        y = (base_height - middle_image.height) // 2
        final_image.paste(middle_image, (x, y), middle_image)
        x += middle_image.width + padding
        
    # Second image
    final_image.paste(right_image, (x, 0))

    buffer = io.BytesIO()
    final_image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


# SAVE THE SHIPS BETWEEN MEMBERS ON EACH SERVER

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_data(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)