import base64
import cv2
import numpy as np
from functools import lru_cache

# Define desired dimensions for resizing
DESIRED_WIDTH, DESIRED_HEIGHT = 800, 600
DESIRED_SIZE = (DESIRED_WIDTH, DESIRED_HEIGHT)

# Define JPEG quality (lower means faster encoding and smaller size)
JPEG_QUALITY = 75

@lru_cache(maxsize=128)
def encode_image_from_bytes(image_data):
    """
    Encodes an image to a base64 string after resizing it to the desired dimensions.
    Utilizes OpenCV for faster processing and caches the result for future use.
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    # Decode the image using OpenCV
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        print("Error: Failed to decode image.")
        return None

    # Check if resizing is necessary
    if img.shape[1] != DESIRED_WIDTH or img.shape[0] != DESIRED_HEIGHT:
        # Resize the image using INTER_AREA for downscaling
        img = cv2.resize(img, DESIRED_SIZE, interpolation=cv2.INTER_AREA)

    # Encode the image to JPEG format
    success, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not success:
        print("Error: Failed to encode image.")
        return None

    # Convert the JPEG buffer to a base64 string
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return encoded_image

def process_images(floorplan_data, live_image_data):
    print("Processing images")

    base64_floorplan = encode_image_from_bytes(floorplan_data) if floorplan_data is not None else None
    base64_live_image = encode_image_from_bytes(live_image_data) if live_image_data is not None else None

    
    # if base64_floorplan is None or base64_live_image is None:
    #     raise ValueError("Failed to process one or both images")
    
    return {
        "floorplan": base64_floorplan,
        "live_image": base64_live_image
    }