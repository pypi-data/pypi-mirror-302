import io
import base64
import os
import numpy as np
from PIL import Image, PngImagePlugin
from PIL.Image import Image as PILImage
from typing import Any
from urllib.request import urlopen


def load_image(data: Any) -> Image:
    """加载图片内容

    Parameters
    ----------
    data : Any

    Returns
    -------
    Image

    Raises
    ------
    ValueError
    """

    if isinstance(data, PILImage):
        img = data
    elif isinstance(data, bytes):
        img = Image.open(io.BytesIO(data))
    elif isinstance(data, np.ndarray):
        img = Image.fromarray(data)
    elif os.path.isfile(data):
        try:
            img = Image.open(data)
        except:
            raise ValueError("Input type {} is not supported.".format(type(data)))
    else:
        try:
            img = Image.open(urlopen(data))
        except:
            raise ValueError("Input type {} is not supported.".format(type(data)))

    try:
        img = img.convert("RGB")
    except:
        pass

    return img


def b64_img(image: PILImage) -> str:
    return "data:image/png;base64," + raw_b64_img(image)


def raw_b64_img(image: PILImage) -> str:
    # XXX controlnet only accepts RAW base64 without headers
    with io.BytesIO() as output_bytes:
        metadata = None
        for key, value in image.info.items():
            if isinstance(key, str) and isinstance(value, str):
                if metadata is None:
                    metadata = PngImagePlugin.PngInfo()
                metadata.add_text(key, value)
        image.save(output_bytes, format="PNG", pnginfo=metadata)

        bytes_data = output_bytes.getvalue()

    return str(base64.b64encode(bytes_data), "utf-8")


def concat(im1: PILImage, im2: PILImage) -> PILImage:
    im1 = im1.convert("RGBA")
    im2 = im2.convert("RGBA")
    new_image = Image.new(mode="RGBA", size=(max(im1.width, im2.width), im1.height + im2.height))
    new_image.paste(im1, (0, 0))
    new_image.paste(im2, (0, im1.height))

    return new_image
