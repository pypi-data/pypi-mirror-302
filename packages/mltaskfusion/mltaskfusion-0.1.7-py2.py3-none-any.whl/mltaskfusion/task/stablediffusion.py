from typing import Any
from .base import _ScikitCompact, TaskModel
from pydantic import BaseModel, Field

TASK_NAME = "stablediffusion"
QUEUE_NAME = "stablediffusion-vb5o"


class StableDiffusionModel(TaskModel):
    """stablediffusion"""

    name: str = TASK_NAME
    queue_name: str = QUEUE_NAME


class StableDiffusionData(BaseModel):
    prompt: str = Field(max_length=4096)
    images: list = Field(default=[], description="list of image, format: image url, bytes, or PIL Image")


class StableDiffusionTask(_ScikitCompact):
    """StableDiffusion task"""

    def handle(self, data: StableDiffusionData) -> Any:
        pass
