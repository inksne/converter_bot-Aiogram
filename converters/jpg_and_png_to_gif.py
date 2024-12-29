from PIL import Image
from io import BytesIO


def convert_image_to_gif(input_data: bytes) -> bytes:
    with Image.open(BytesIO(input_data)) as img:
        img = img.convert("RGBA")
        output = BytesIO()
        img.save(output, format="GIF")
        output.seek(0)
        return output.read()


def convert_gif_to_image(input_data: bytes, output_format="PNG") -> bytes:
    with Image.open(BytesIO(input_data)) as img:
        output = BytesIO()
        img.save(output, format=output_format.upper())
        output.seek(0)
        return output.read()