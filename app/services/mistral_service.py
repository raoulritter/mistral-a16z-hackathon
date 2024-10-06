import requests
import json
from core.config import settings
from requests.exceptions import SSLError, RequestException
import time

class MistralService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_prompt(self, task: str, base64_floor_plan: str, base64_live_image: str, transcription: str) -> list:
        prompt = f"""
        You are a helpful visual impairment assistant. You are given a floor plan, a live image, and an audio transcription.
        Using the floor plan, live image, and audio transcription provided, perform the following:

        1. **Infer the current position** of the person based on the live image and audio transcription.
        2. **Determine the target task** they want to accomplish based on the audio transcription: "{transcription}"
        3. **Plan the optimal path** to reach the target location necessary to complete the task.
        4. **Provide detailed navigation instructions** similar to Google Maps, including turns and approximate distances in steps.

        Audio Transcription: {transcription}

        **Please provide the output in the following JSON format:**

        ```{{
        "current_location": "Inferred current location",
        "target_task": "Task determined from audio transcription",
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
        "current_action": "Current action being performed"
        }}
        ```

        **Notes:**
        - Ensure that each step in the plan is clear and actionable.
        - You are in Europe, so the fire exit is green.
        - If there are multiple ways to perform a step, choose the most efficient one based on the floor plan.
        - If additional information is required to complete the task, indicate what is needed.
        - Provide detailed navigation instructions similar to Google Maps, including turns and approximate distances in steps.
        - Consider any relevant information from the audio transcription when planning the path and actions.

        Please generate the structured JSON response based on the above instructions.
        """

        return [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_floor_plan}"
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_live_image}"
                    }
                ]
            }
        ]

    def send_request(self, messages, max_retries=3, retry_delay=5):
        data = {
            "model": self.model,
            "messages": messages
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
                response.raise_for_status()
                print(f"Response: {response}")

                return response
            except (SSLError, RequestException) as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to connect to Mistral API after {max_retries} attempts: {str(e)}")
                print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    def process_task(self, task: str, base64_floor_plan: str, base64_live_image: str, transcription: str) -> dict:
        messages = self.create_prompt(task, base64_floor_plan, base64_live_image, transcription)
        # response = self.send_request(messages)
        try:
            response = self.send_request(messages)
        except Exception as e:
            print(f"Error: {str(e)}")
            return {"error": "Failed to process the task"}
        
        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0]['message']['content']
            # Extract JSON from the content (assuming it's wrapped in ```json ... ```)
            json_start = content.find('```json') + 7
            json_end = content.rfind('```')
            json_str = content[json_start:json_end].strip()
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON response"}
        else:
            return {"error": "Unable to process the task"}

# Initialize the service
mistral_service = MistralService(settings.MISTRAL_API_KEY)

# class MistralService:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.url = "https://api.mistral.ai/v1/chat/completions"
#         self.headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.api_key}"
#         }

#     def create_prompt(self, task: str, base64_floor_plan: str, base64_live_image: str) -> list:
#         prompt = f"""
#         Using the floor plan provided below and the live image, perform the following:

#         1. **Infer the current position** of the person based on the live image.
#         2. **Determine the target task** they want to accomplish (e.g., getting coffee).
#         3. **Plan the optimal path** to reach the target location necessary to complete the task.

#         **Please provide the output in the following JSON format:**

#         ```{{
#         "current_location": "Dining Area",
#         "target_task": "{task}",
#         "plan": [
#             {{
#             "step_number": 1,
#             "action": "Identify Current Location",
#             "description": "Confirm that the user is in the Dining Area based on the live image and floor plan."
#             }},
#             {{
#             "step_number": 2,
#             "action": "Navigate to Kitchen",
#             "description": "Head towards the Kitchen, which is adjacent to the Dining Area."
#             }},
#             {{
#             "step_number": 3,
#             "action": "Locate Coffee Maker",
#             "description": "Find the coffee maker on the kitchen countertops, specifically in the 'coffee' zone to the left of the kitchen."
#             }},
#             {{
#             "step_number": 4,
#             "action": "Prepare Coffee",
#             "description": "Use the coffee maker to brew coffee."
#             }}
#         ],
#         "current_action": "Identifying current location"
#         }}
#         ```

#         **Notes:**
#         - Ensure that each step in the plan is clear and actionable.
#         - If there are multiple ways to perform a step, choose the most efficient one based on the floor plan.
#         - If additional information is required to complete the task, indicate what is needed.
#         - Provide detailed navigation instructions similar to Google Maps, including turns and approximate distances in steps.

#         Please generate the structured JSON response based on the above instructions.
#         """

#         return [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": prompt
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": f"data:image/jpeg;base64,{base64_floor_plan}"
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": f"data:image/jpeg;base64,{base64_live_image}"
#                     }
#                 ]
#             }
#         ]

#     def send_request(self, messages: list) -> dict:
#         data = {
#             "model": "pixtral-12b-2409",
#             "messages": messages
#         }

#         response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
#         return response.json()

#     def process_task(self, task: str, base64_floor_plan: str, base64_live_image: str) -> dict:
#         messages = self.create_prompt(task, base64_floor_plan, base64_live_image)
#         response = self.send_request(messages)
        
#         if 'choices' in response and len(response['choices']) > 0:
#             content = response['choices'][0]['message']['content']
#             # Extract JSON from the content (assuming it's wrapped in ```json ... ```)
#             json_start = content.find('```json') + 7
#             json_end = content.rfind('```')
#             json_str = content[json_start:json_end].strip()
            
#             try:
#                 return json.loads(json_str)
#             except json.JSONDecodeError:
#                 return {"error": "Failed to parse JSON response"}
#         else:
#             return {"error": "Unable to process the task"}

# # Initialize the service
# mistral_service = MistralService(settings.MISTRAL_API_KEY)


class MistralService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    def create_prompt(self, task: str, base64_floor_plan: str, base64_live_image: str, transcription: str) -> list:
        prompt = f"""
        Using the floor plan, live image, and audio transcription provided, perform the following:

        1. **Infer the current position** of the person based on the live image and audio transcription.
        2. **Determine the target task** they want to accomplish based on the audio transcription: "{transcription}"
        3. **Plan the optimal path** to reach the target location necessary to complete the task.

        Audio Transcription: {transcription}

        **Please provide the output in the following JSON format:**

        ```{{
        "current_location": "Inferred current location",
        "target_task": "Task determined from audio transcription",
        "plan": [
            {{
            "step_number": 1,
            "action": "Action description",
            "description": "Detailed description of the action"
            }},
            // Additional steps as needed
        ],
        "current_action": "Current action being performed"
        }}
        ```

        **Notes:**
        - Ensure that each step in the plan is clear and actionable.
        - If there are multiple ways to perform a step, choose the most efficient one based on the floor plan.
        - If additional information is required to complete the task, indicate what is needed.
        - Provide detailed navigation instructions similar to Google Maps, including turns and approximate distances in steps.
        - Consider any relevant information from the audio transcription when planning the path and actions.

        Please generate the structured JSON response based on the above instructions.
        """

        return [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_floor_plan}"
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_live_image}"
                    }
                ]
            }
        ]
    def send_request(self, messages: list) -> dict:
        data = {
            "model": "pixtral-12b-2409",
            "messages": messages
        }

        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        return response.json()

    def process_task(self, task: str, base64_floor_plan: str, base64_live_image: str, transcription: str) -> dict:
        messages = self.create_prompt(task, base64_floor_plan, base64_live_image, transcription)
        response = self.send_request(messages)
        
        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0]['message']['content']
            print(f"content: {content}")
            # Extract JSON from the content (assuming it's wrapped in ```json ... ```)
            json_start = content.find('```json') + 7
            json_end = content.rfind('```')
            json_str = content[json_start:json_end].strip()
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON response"}
        else:
            return {"error": "Unable to process the task"}
# Initialize the service
mistral_service = MistralService(settings.MISTRAL_API_KEY)

    


