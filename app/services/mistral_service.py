import requests
import json
from core.config import settings

# class MistralService:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.url = "https://api.mistral.ai/v1/chat/completions"
#         self.headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.api_key}"
#         }

#     def create_prompt(self, transcription: str, timestamps: list) -> str:
#         prompt = f"""You are an AI assistant for a visually impaired person. Based on the following audio transcription, provide a clear and concise description of the environment, potential hazards, and important information that would be helpful for navigation and understanding the surroundings. Focus on:

# 1. Spatial layout and obstacles
# 2. People and activities in the area
# 3. Potential hazards or safety concerns
# 4. Relevant sounds or audio cues
# 5. Any text or signage mentioned in the audio

# Please organize your response in short, easy-to-understand instructions."

# Transcription: {transcription}

# Key timestamps:
# """
#         for chunk in timestamps:
#             prompt += f"- {chunk['timestamp']}: {chunk['text']}\n"
        
#         prompt += "\nPlease provide a helpful description for the visually impaired person:"
        
#         return prompt

#     def send_request(self, prompt: str) -> dict:
#         data = {
#             "model": "mistral-small-latest",
#             "temperature": 0.7,
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         }

#         response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
#         return response.json()

#     def process_transcription(self, transcription: str, timestamps: list) -> str:
#         prompt = self.create_prompt(transcription, timestamps)
#         # print(prompt)
#         # pdb.set_trace()
#         response = self.send_request(prompt)
        
#         # Extract the assistant's message from the response
#         if 'choices' in response and len(response['choices']) > 0:
#             return response['choices'][0]['message']['content']
#         else:
#             return "Error: Unable to process the transcription."

# Usage example:
# mistral_service = MistralService(settings.MISTRAL_API_KEY)
# result = mistral_service.process_transcription(transcription, timestamps)
import requests
import json
from core.config import settings

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

    


