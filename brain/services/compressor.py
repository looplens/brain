from PIL import Image
import io
from moviepy.editor import VideoFileClip


class MediaCompressor:
    @staticmethod
    async def compress_image(content: bytes) -> bytes:
        image = Image.open(io.BytesIO(content))
        compressed_image = io.BytesIO()
        image.save(compressed_image, format="JPEG", quality=40)
        return compressed_image.getvalue()

    @staticmethod
    def compress_video(input_path, output_path, scale_factor=0.5):
        try:
            video_clip = VideoFileClip(input_path)

            width = int(video_clip.size[0] * scale_factor)
            height = int(video_clip.size[1] * scale_factor)
            compressed_clip = video_clip.resize((width, height))

            audio_clip = video_clip.audio
            final_clip = compressed_clip.set_audio(audio_clip)

            final_clip.write_videofile(
                output_path, codec="libx264", audio_codec="aac", fps=24
            )

            video_clip.close()
            compressed_clip.close()
            final_clip.close()

            return True

        except Exception as e:
            return False, f"Hata: {str(e)}"
