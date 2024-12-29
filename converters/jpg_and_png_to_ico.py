from PIL import Image
from io import BytesIO


async def image_to_ico(image_data: bytes) -> bytes:
    image = Image.open(BytesIO(image_data))
    with BytesIO() as output:
        image.save(output, format="ICO", sizes=[(256, 256)])
        return output.getvalue()


async def ico_to_image(ico_data: bytes) -> bytes:
    with BytesIO(ico_data) as input:
        image = Image.open(input)
        with BytesIO() as output:
            image.save(output, format="PNG")
            return output.getvalue()