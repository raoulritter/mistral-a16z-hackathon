import os
import cv2
import base64

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

def encode_image(image_path):
    """
    Encodes an image file to base64.

    Parameters:
    - image_path (str): The file path of the image to encode.

    Returns:
    - str: Base64 encoded string of the image, or None if encoding fails.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

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