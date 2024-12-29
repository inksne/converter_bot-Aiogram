from PIL import Image
from io import BytesIO


def convert_image(input_data: bytes, output_format: str) -> bytes:
    with Image.open(BytesIO(input_data)) as img:
        if output_format.upper() == 'JPEG' and img.mode != 'RGB':
            img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format=output_format.upper())
        output.seek(0)
        return output.read()