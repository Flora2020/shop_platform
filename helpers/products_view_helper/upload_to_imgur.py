import os
from typing import Union
from flask_imgur.flask_imgur import Imgur

imgur_handler = Imgur(client_id=os.environ.get('IMGUR_ID'))


def upload_to_imgur(image: bytes) -> Union[str, None]:
    if not image:
        return None

    image_data = imgur_handler.send_image(image)
    return image_data['data']['link'] if image_data['success'] else None
