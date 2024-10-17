import logging
import time
from mltaskfusion.utils import helper
from .vllm import VllmData, VllmModel, TASK_NAME as VLLM_TASK_NAME, VllmTask
from .ollama import OllamaData, OllamaModel, TASK_NAME as OLLAMA_TASK_NAME, OllamaTask
from .stablediffusion import StableDiffusionData, StableDiffusionModel, TASK_NAME as STABLEDIFFUSION_TASK_NAME
from mltaskfusion.db import queue_client, Job

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
task_names = [OLLAMA_TASK_NAME, STABLEDIFFUSION_TASK_NAME, VLLM_TASK_NAME]


class Task:
    def __init__(self, task_name: str):
        self.task_name = task_name

        if self.task_name == OLLAMA_TASK_NAME:
            task = OllamaModel(id=helper.unique_id())
            self.data_class = OllamaData
            self.task_cli = OllamaTask()
        elif self.task_name == STABLEDIFFUSION_TASK_NAME:
            task = StableDiffusionModel(id=helper.unique_id())
            self.data_class = StableDiffusionData
        else:
            task = VllmModel(id=helper.unique_id())
            self.data_class = VllmData
            self.task_cli = VllmTask()

        self.task = task
        self.queue_cli = queue_client(queue_name=task.queue_name)

    def handle(self):
        """handle"""

        logging.info("[task: %s] starting ...", self.task_name)

        while True:
            job = self.queue_cli.pop()

            if not job:
                time.sleep(2)
                continue

            try:
                self._handle_job(job)
            except Exception as ex:
                # TODO 记录日志
                pass

    def _handle_job(self, job: Job):
        """handle job"""

        try:
            job.delete()
            data = self.data_class.model_validate_json(job.get_raw_body())
            logging.info("[task: %s] Processing job: %s ...", self.task_name, data.id)
            result = self.task_cli.handle(data)
            logging.info("[task: %s] Processed job: %s", self.task_name, data.id)
        except Exception as e:
            result = ""
        self.queue_cli.update_result(task_id=data.id, data={"content": result})


def task_pipeline(task_name: str):
    """任务管道

    Parameters
    ----------
    task_name : str
        任务名称
    """

    Task(task_name=task_name).handle()
