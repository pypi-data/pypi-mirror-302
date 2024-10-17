import json
from pydantic import BaseModel, Field
from abc import abstractmethod, ABC


class QueueJobModel(BaseModel):
    """队列任务模型"""

    id: str = Field(description="任务ID")
    data: dict = Field(description="任务数据, json 后数据结构")


class Job:
    """队列Job"""

    def __init__(self, worker, job, reserved):
        self.worker = worker
        self.job = job
        self.reserved = reserved

    def delete(self):
        """释放任务"""
        try:
            self.worker.delete_reserved(self)
        except:
            pass

    def get_reserved_job(self):
        """释放任务标识"""
        return self.reserved

    def to_json(self):
        """获取格式化后的job数据"""

        return json.loads(self.job)

    def get_raw_body(self):
        """获取格式化后的job数据"""

        return self.job


class _ScikitCompact(ABC):

    @abstractmethod
    def push(self, job: QueueJobModel):
        raise NotImplementedError()

    @abstractmethod
    def push_and_response(self, job: QueueJobModel):
        raise NotImplementedError()

    @abstractmethod
    def pop(self, islast: bool = False):
        raise NotImplementedError()

    @abstractmethod
    def update_result(self, task_id: str, data: dict, expired_seconds: int = 1800) -> bool:
        raise NotImplementedError()
