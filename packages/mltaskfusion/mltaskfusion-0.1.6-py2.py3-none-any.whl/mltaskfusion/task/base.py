from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    """任务基础模型"""

    name: str = Field(description="任务名称")
    queue_name: str = Field(description="队列名称")
    status: str = Field(default="pending", description="任务状态", enum=["pending", "running", "success", "failed"])
    data: dict = Field(default={}, description="任务数据", example={"a": 1, "b": 2}, title="任务数据")


class BaseData(BaseModel):
    """基础 数据结构"""

    id: str = Field(description="任务ID")


class _ScikitCompact(ABC):

    @abstractmethod
    def handle(self, data: Any):  # -> Any:
        raise NotImplementedError()
