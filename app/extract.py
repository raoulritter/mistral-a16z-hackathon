import cv2
import os

video_path = "/Users/raoulritter/Downloads/IMG_6794.MOV"

def extract_frames(video_path, output_dir, fps=4):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get the video's frame rate
    video_fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate the frame interval
    frame_interval = int(video_fps / fps)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    frame_count = 0
    saved_count = 0
    
    while True:
        success, frame = video.read()
        if not success:
            break
        
        if frame_count % frame_interval == 0:
            # Save the frame as an image file
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        
        frame_count += 1
    
    video.release()
    print(f"Extracted {saved_count} frames from {os.path.basename(video_path)}")

# Process the specified .mov file
video_name = os.path.splitext(os.path.basename(video_path))[0]
output_dir = f"{video_name}_frames"
extract_frames(video_path, output_dir)