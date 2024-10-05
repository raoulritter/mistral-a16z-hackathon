import io
import json
import os
import base64
import cv2  # Added OpenCV for faster image processing
from functools import lru_cache  # For efficient caching
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables.")

# Define the model to use
model = "mistral-small-latest"  # You can adjust this as needed

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Task definition
task = """Hey, I would like to get myself a coffee. Can you help me please."""

# Define desired dimensions for resizing
DESIRED_WIDTH, DESIRED_HEIGHT = 800, 600
DESIRED_SIZE = (DESIRED_WIDTH, DESIRED_HEIGHT)

# Define JPEG quality (lower means faster encoding and smaller size)
JPEG_QUALITY = 75

@lru_cache(maxsize=128)
def encode_image(image_path):
    """
    Encodes an image to a base64 string after resizing it to the desired dimensions.
    Utilizes OpenCV for faster processing and caches the result for future use.
    """
    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} was not found.")
        return None

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

def get_cached_image(image_path):
    """
    Retrieves the cached base64-encoded image if available.
    Otherwise, encodes the image and caches the result.
    """
    return encode_image(image_path)

# Initialize a cache dictionary (handled by lru_cache)

# Paths to your images
reduced_image_path = "data/preload/floorplan_reduced.jpg"
live_image_path = "data/live/live1_r2.jpg"

# Encode images
base64_image = get_cached_image(reduced_image_path)
if base64_image is None:
    raise ValueError(f"Failed to encode image: {reduced_image_path}")

base64_img_live = get_cached_image(live_image_path)
if base64_img_live is None:
    raise ValueError(f"Failed to encode image: {live_image_path}")



# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Define the messages for the chat
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""
    Using the floor plan provided below and the live image, perform the following:

    1. **Infer the current position** of the person based on the live image.
    2. **Determine the target task** they want to accomplish (e.g., getting coffee).
    3. **Plan the optimal path** to reach the target location necessary to complete the task.

    **Please provide the output in the following JSON format:**

            ```{{
            "current_location": "Dining Area",
            "target_task": "Get Coffee",
            "plan": [
                {{
                "step_number": 1,
                "action": "Identify Current Location",
                "description": "Confirm that the user is in the Dining Area based on the live image and floor plan."
                }},
                {{
                "step_number": 2,
                "action": "Navigate to Kitchen",
                "description": "Head towards the Kitchen, which is adjacent to the Dining Area."
                }},
                {{
                "step_number": 3,
                "action": "Locate Coffee Maker",
                "description": "Find the coffee maker on the kitchen countertops, specifically in the 'coffee' zone to the left of the kitchen."
                }},
                {{
                "step_number": 4,
                "action": "Prepare Coffee",
                "description": "Use the coffee maker to brew coffee."
                }}
            ],
            "current_action": "Identifying current location"
            }}
    ```

    **Notes:**
    - Ensure that each step in the plan is clear and actionable.
    - If there are multiple ways to perform a step, choose the most efficient one based on the floor plan.
    - If additional information is required to complete the task, indicate what is needed.

    Please generate the structured JSON response based on the above instructions.
"""
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_img_live}"
            }
        ]
    }
]


stream_response = client.chat.stream(
    model = model,
    messages = messages
)


json_output = ""
for chunk in stream_response:
    json_output += chunk.data.choices[0].delta.content
    # print(chunk.data.choices[0].delta.content, end='', flush=True)

if json_output.strip():
    try:
        # Debug: Print the JSON output to check its structure
        print("Raw JSON output:", json_output.strip())

        if json_output.startswith('```json') and json_output.endswith('```'):
            json_output = json_output[len('```json'): -3].strip()
        task_data = json.loads(json_output.strip())
        print(task_data['current_location'])
        # Save the task_data to a variable or database
        # Example:
        # current_task = task_data
        print("Task data successfully parsed and saved.")
    except json.JSONDecodeError as e:
        # Print the error message and the problematic JSON
        print("Received invalid JSON data after stripping.")
        print("Error message:", e)
        print("Problematic JSON:", json_output.strip())

# print(task_data)



# if 'task_data' in locals():
#     print("Current Location:", task_data.get("current_location", "Unknown"))
#     print("Action:", task_data.get("action", "Unknown"))
#     print("Current Action:", task_data.get("current_action", "Unknown"))
# else:
#     print("No task data available to display.")


# json_output = ""
# for chunk in stream_response:
#     json_output += chunk.data.choices[0].delta.content
# if json_output.strip():
#     try:
#         task_data = json.loads(json_output)
#         print("Current Location:", task_data.get("current_location", "Unknown"))
#         print("Target Task:", task_data.get("target_task", "Unknown"))
#         print("Current Action:", task_data.get("current_action", "Unknown"))
#     except json.JSONDecodeError:
#         print("Received invalid JSON data.")


# Store the JSON output from the API call in a variable
# for chunk in stream_response:
#     json_output = chunk.data.choices[0].delta.content
#     if json_output.strip():  # Check if the chunk is not empty
#         try:
#             # Assuming json_output is a valid JSON string, parse it
#             task_data = json.loads(json_output)
            
#             # Print the current location, target task, and current action
#             print("Current Location:", task_data.get("current_location", "Unknown"))
#             print("Target Task:", task_data.get("target_task", "Unknown"))
#             print("Current Action:", task_data.get("current_action", "Unknown"))
#         except json.JSONDecodeError:
#             print("Received invalid JSON data.")



# we now need to manage state
# i.e., where was I before, where am i now... have i completed tasks in my history and so on...
# 