import requests
import json

def create_prompt(transcription, timestamps):
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

def send_to_mistral(prompt, api_key):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
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

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()