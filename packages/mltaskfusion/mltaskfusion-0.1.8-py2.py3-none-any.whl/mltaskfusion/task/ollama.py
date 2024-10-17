from typing import Any
from pydantic import BaseModel, Field
from openai import OpenAI

from mltaskfusion.utils import config, image
from .base import _ScikitCompact, BaseData, TaskModel

TASK_NAME = "ollama"
QUEUE_NAME = "ollama-h4cv"


class OllamaModel(TaskModel):
    """ollama"""

    name: str = TASK_NAME
    queue_name: str = QUEUE_NAME


class OllamaData(BaseData):
    prompt: str = Field(max_length=4096)
    images: list = Field(default=[], description="list of image, format: image url, bytes, or PIL Image")
    max_tokens: int = 4096
    ml_model_name: str = "minicpm-v:latest"


class OllamaTask(_ScikitCompact):
    """Ollama task"""

    def __init__(self):
        self.client = OpenAI(
            base_url=config.config("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key="EMPTY",  # required, but unused
        )

    def handle(self, data: OllamaData) -> Any:
        new_image = None

        for img in data.images:
            if not new_image:
                new_image = image.load_image(img)
            else:
                new_image = image.concat(im1=new_image, im2=image.load_image(img))

        content = []

        if new_image:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": image.b64_img(image=new_image), "detail": "low"},
                }
            )

        content.append(
            {
                "type": "text",
                "text": data.prompt,
            }
        )

        chat_completion_from_base64 = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model=data.ml_model_name,
            max_tokens=data.max_tokens,
        )
        content = chat_completion_from_base64.choices[0].message.content.split("<|eot_id|>", maxsplit=1)[0]
        return content
