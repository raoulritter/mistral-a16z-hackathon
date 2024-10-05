import json
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables.")

# Initialize the Mistral client
client = Mistral(api_key=api_key)

async def generate_guidance(transcription, image_description):
    model = "pixtral-12b-2409"  # You can adjust this as needed

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
    Using the floor plan provided below and the live image, perform the following:

    1. **Infer the current position** of the person based on the live image.
    2. **Determine the target task** they want to accomplish
    3. **Plan the optimal path** to reach the target location necessary to complete the task.
    4. **Generate a detailed step-by-step plan** for the task. 
    5. **Indicate the current action** the person is taking.

    The target task is: {transcription}

    **Please provide the output in the following JSON format:**

    {{
        "current_location": "Dining Area",
        "target_task": "Getting Coffee",
        "plan": [
            {{
                "step_number": 1,
                "action": "Identify Current Location",
                "description": "Confirm that the user is in the Dining Area based on the live image and floor plan."
            }},
            // ... more steps ...
        ],
        "current_action": "Identifying current location"
    }}

    **Notes:**
    - Ensure that each step in the plan is clear and actionable.
    - If there are multiple ways to perform a step, choose the most efficient one based on the floor plan.
    - If additional information is required to complete the task, indicate what is needed.
    - Provide detailed navigation instructions similar to Google Maps, including turns and approximate distances in steps.

    Please generate the structured JSON response based on the above instructions.
    """
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{image_description}"
                }
            ]
        }
    ]

    stream_response = client.chat.stream(
        model=model,
        messages=messages
    )

    json_output = ""
    for chunk in stream_response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            json_output += chunk.choices[0].delta.content

    try:
        if json_output.startswith('```json') and json_output.endswith('```'):
            json_output = json_output[len('```json'): -3].strip()
        task_data = json.loads(json_output.strip())
        return task_data
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None

# # You can keep the process_chat function here if needed
# def process_chat(prompt, mistral_api_key):
#     # Process chat using Mistral API
#     # Return chat result
#     pass