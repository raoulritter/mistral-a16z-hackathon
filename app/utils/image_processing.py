import os
import cv2
import base64
import cv2
import numpy as np

# Define desired dimensions for resizing
DESIRED_WIDTH, DESIRED_HEIGHT = 800, 600
DESIRED_SIZE = (DESIRED_WIDTH, DESIRED_HEIGHT)

# Define JPEG quality (lower means faster encoding and smaller size)
JPEG_QUALITY = 75

def reduce_image_size(input_path, output_path, desired_width=400, desired_height=300, jpeg_quality=75):
    """
    Reduces the size of the image located at input_path and saves it to output_path.

    Parameters:
    - input_path (str): The file path of the original image.
    - output_path (str): The file path where the resized image will be saved.
    - desired_width (int): The target width for the resized image. Default is 400.
    - desired_height (int): The target height for the resized image. Default is 300.
    - jpeg_quality (int): The quality of the saved JPEG image (0 to 100). Default is 75.

    Returns:
    - bool: True if the image was successfully resized and saved, False otherwise.
    """
    if not os.path.exists(input_path):
        print(f"Error: The file {input_path} was not found.")
        return False

    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Failed to read image {input_path}.")
        return False

    # Resize the image if it doesn't match the desired dimensions
    if img.shape[1] != desired_width or img.shape[0] != desired_height:
        try:
            img = cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_AREA)
            print(f"Image resized to {desired_width}x{desired_height}.")
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    else:
        print("Image already matches the desired dimensions. No resizing needed.")

    # Save the resized image with the specified JPEG quality
    try:
        success = cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
        if not success:
            print(f"Error: Failed to save image to {output_path}.")
            return False
        print(f"Image successfully saved to {output_path} with JPEG quality {jpeg_quality}.")
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

    """
    Encodes an image to a base64 string after resizing it to the desired dimensions.
    Utilizes OpenCV for faster processing and caches the result for future use.
    """
    # if not os.path.exists(image_path):
    #     pdb.set_trace()
    #     print(f"Error: The file {image_path} was not found.")
    #     return None

    # Read the image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Failed to read image {image_path}.")
        
        return None

    # Check if resizing is necessary
    if img.shape[1] != DESIRED_WIDTH or img.shape[0] != DESIRED_HEIGHT:
        # Resize the image using INTER_AREA for downscaling
        img = cv2.resize(img, DESIRED_SIZE, interpolation=cv2.INTER_AREA)

    # Encode the image to JPEG format
    success, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not success:
        print(f"Error: Failed to encode image {image_path}.")
        return None

    # Convert the JPEG buffer to a base64 string
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return encoded_image


def encode_image(image_input):
    """
    Encodes an image to a base64 string after resizing it to the desired dimensions.
    Utilizes OpenCV for faster processing.
    
    :param image_input: Either a file path (str) or image data (bytes)
    :return: Base64 encoded string of the image
    """
    if isinstance(image_input, str):
        # If input is a file path, read the image using OpenCV
        img = cv2.imread(image_input)
    elif isinstance(image_input, bytes):
        # If input is bytes, convert to numpy array and decode
        nparr = np.frombuffer(image_input, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    else:
        print("Error: Invalid input type for image.")
        return None

    if img is None:
        print("Error: Failed to read image.")
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

def get_cached_image(image_path):
    """
    Retrieves a cached base64 encoded image or encodes it if not cached.

    Parameters:
    - image_path (str): The file path of the image.

    Returns:
    - str: Base64 encoded string of the image, or None if encoding fails.
    """
    # In a real application, you might want to implement actual caching here
    # For simplicity, we're just encoding the image every time
    return encode_image(image_path)

# Example usage (can be removed in production)
if __name__ == "__main__":
    input_image_path = "data/preload/floorplan.jpg"
    output_image_path = "data/preload/floorplan_reduced.jpg"
    reduce_image_size(input_image_path, output_image_path)
    encoded_image = get_cached_image(output_image_path)
    if encoded_image:
        print("Image successfully encoded.")
    else:
        print("Failed to encode image.")