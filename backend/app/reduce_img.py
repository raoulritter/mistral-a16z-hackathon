import os
import cv2


def reduce_image_size(input_path, output_path, desired_width=400, desired_height=300, jpeg_quality=75):
    """
    Reduces the size of the image located at input_path and saves it to output_path.

    Parameters:
    - input_path (str): The file path of the original image.
    - output_path (str): The file path where the resized image will be saved.
    - desired_width (int): The target width for the resized image. Default is 800.
    - desired_height (int): The target height for the resized image. Default is 600.
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

# Example usage
if __name__ == "__main__":
    input_image_path = "data/preload/floorplan.jpg"
    output_image_path = "data/preload/floorplan_reduced.jpg"
    reduce_image_size(input_image_path, output_image_path)
