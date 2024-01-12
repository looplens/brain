from moviepy.editor import VideoFileClip

def compress_video(input_path, output_path, scale_factor=0.5):
  try:
    video_clip = VideoFileClip(input_path)

    width = int(video_clip.size[0] * scale_factor)
    height = int(video_clip.size[1] * scale_factor)
    compressed_clip = video_clip.resize((width, height))

    audio_clip = video_clip.audio

    final_clip = compressed_clip.set_audio(audio_clip)

    final_clip.write_videofile(
      output_path,
      codec="libx264",
      audio_codec="aac",
      fps=24
    )

    video_clip.close()
    compressed_clip.close()
    final_clip.close()

    return True

  except Exception as e:
    return False, f"Hata: {str(e)}"
















# import cv2
# import numpy as np

# def compress_video(input_path, output_path):
#   try:
#     cap = cv2.VideoCapture(input_path)
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")

#     scale_factor = 0.5
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale_factor)
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale_factor)
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

#     while True:
#       ret, frame = cap.read()
#       if not ret:
#         break

#       resized_frame = cv2.resize(frame, (width, height))

#       out.write(resized_frame)

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

#     return True
#   except Exception as e:
#     print(e)
#     return False
