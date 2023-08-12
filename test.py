import cv2
import numpy as np
import subprocess

def apply_effects(image, shadow_intensity=0.7, brightness_factor=1.2):
    shadow = np.copy(image)
    shadow = cv2.GaussianBlur(shadow, (21, 21), 0)
    shadow = (shadow_intensity * shadow).astype(np.uint8)

    brightened_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
    
    combined = cv2.addWeighted(brightened_image, 1, shadow, 0.5, 0)
    return combined

def adjust_saturation(image, saturation_factor=1.0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def set_black_point(image, threshold=5):
    image[image < threshold] = 0
    return image



input_file = 'D:\mixer bot/clip.mp4'
output_file = 'output_video_with_effects_and_audio.mp4'

video_capture = cv2.VideoCapture(input_file)
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
frame_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

# Specify the paths to ffmpeg and ffprobe executables


# Add noise to the audio

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    saturated_frame = adjust_saturation(frame, saturation_factor=1.5)
    black_point_frame = set_black_point(saturated_frame, threshold=5)
    final_frame = apply_effects(black_point_frame, shadow_intensity=0.7, brightness_factor=1.2)
    
    output_video.write(final_frame)

video_capture.release()
output_video.release()

# Export the final audio with noise
output_audio_path = 'output_audio_with_noise.mp3'


print('Done')