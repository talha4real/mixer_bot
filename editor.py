

def mix_video(video,folder_id):
    # URL to download the video from Google Drive
    url = f"https://drive.google.com/uc?id={video['id']}"
    output_path = f"./temp/{video['name']}"
    gdown.download(url, output_path, quiet=False)
    video_clip = VideoFileClip(output_path)
    noisy_video_clip = video_clip.fl_image(add_noise)

    # Apply saturation effect
    saturated_clip = video_clip.fx(colorx.colorx, 1.5)

    # Output video path
    output_path = f"./output/{video['name']}"

    # Write the modified clip to an output file
    saturated_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
 
    # Close the video clips
    video_clip.close()
    saturated_clip.close()
  