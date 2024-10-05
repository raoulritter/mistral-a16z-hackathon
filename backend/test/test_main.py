import io
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Update the paths to match your repository structure
TEST_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'live', 'live1.jpg')
TEST_AUDIO_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'live', 'audio', 'audio1.mp3')
TEST_FLOORPLAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'preload', 'floorplan.jpg')


def test_transcribe_endpoint():
    # Create a mock audio file
    with open(TEST_AUDIO_PATH, "rb") as audio_file:
        audio_content = audio_file.read()
    
    audio_file = io.BytesIO(audio_content)

    response = client.post(
        "/transcribe",
        files={"audio": ("audio.mp3", audio_file, "audio/mp3")}
    )

    assert response.status_code == 200
    assert "transcription" in response.json()

# def test_guide_endpoint():
#     # Use the actual image file
#     with open(TEST_IMAGE_PATH, "rb") as image_file:
#         image_content = image_file.read()
    
#     image_file = io.BytesIO(image_content)
#     transcription = "This is a test transcription"

#     response = client.post(
#         "/guide",
#         files={
#             "image": ("live1.jpg", image_file, "image/jpeg"),
#         },
#         data={"transcription": transcription}
#     )

#     assert response.status_code == 200
#     assert "guidance" in response.json()


def test_guide_endpoint():
    # Use the actual image file
    with open(TEST_IMAGE_PATH, "rb") as image_file:
        image_content = image_file.read()
    
    image_file = io.BytesIO(image_content)
    transcription = "This is a test transcription"

    response = client.post(
        "/guide",
        files={
            "image": ("live1.jpg", image_file, "image/jpeg"),
        },
        data={"transcription": transcription}
    )

    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")

    # Ensure the response is not a streaming response
    assert not response.is_stream, "Unexpected streaming response"

    # Read the response content
    content = response.content
    print(f"Response content: {content[:100]}...")  # Print first 100 characters

    assert response.status_code == 200
    response_json = response.json()
    assert "guidance" in response_json

    print(f"Guidance: {response_json['guidance']}")




# Add more tests as needed

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])