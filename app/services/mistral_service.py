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

    def create_prompt(self, transcription: str, timestamps: list) -> str:
        prompt = f"""You are an AI assistant for a visually impaired person. Based on the following audio transcription, provide a clear and concise description of the environment, potential hazards, and important information that would be helpful for navigation and understanding the surroundings. Focus on:

1. Spatial layout and obstacles
2. People and activities in the area
3. Potential hazards or safety concerns
4. Relevant sounds or audio cues
5. Any text or signage mentioned in the audio

Please organize your response in short, easy-to-understand instructions."

Transcription: {transcription}

Key timestamps:
"""
        for chunk in timestamps:
            prompt += f"- {chunk['timestamp']}: {chunk['text']}\n"
        
        prompt += "\nPlease provide a helpful description for the visually impaired person:"
        
        return prompt

    def send_request(self, prompt: str) -> dict:
        data = {
            "model": "mistral-small-latest",
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        return response.json()

    def process_transcription(self, transcription: str, timestamps: list) -> str:
        prompt = self.create_prompt(transcription, timestamps)
        response = self.send_request(prompt)
        
        # Extract the assistant's message from the response
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return "Error: Unable to process the transcription."

# Usage example:
# mistral_service = MistralService(settings.MISTRAL_API_KEY)
# result = mistral_service.process_transcription(transcription, timestamps)
