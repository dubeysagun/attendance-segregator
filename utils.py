# utils.py
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((28, 28))               # Resize to match MNIST format
    image_np = np.array(image).flatten()         # Flatten the image
    return image_np / 255.0                      # Normalize
