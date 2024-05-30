from PIL import Image
import io
import base64

def compress_image(image_bytes, quality=85):
    image = Image.open(io.BytesIO(image_bytes))
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=quality)
    return buffer.getvalue()

def convert_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')