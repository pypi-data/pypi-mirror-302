# ml-task-fusion

跨服务器llm和stable diffusion任务调用分发.

## Installation

```bash
pip install mltaskfusion
```

在 /etc/.ml-task-fusion/main.conf 中增加以下配置:

```conf
# redis 配置
REDIS_HOST="192.168.9.5"
REDIS_PASSWORD="123456"
REDIS_PORT=16379

# vllm 框架地址
VLLM_BASE_URL="http://118.145.131.117:8000/v1"
```

启动服务:

```bash
mltaskfusion-cli --models=vllm --config=/etc/.ml-task-fusion/main.conf
```

## Usage

### Basic Example

```python

import os
from mltaskfusion.task.vllm import VllmData, VllmModel
from mltaskfusion.db import queue_client, QueueJobModel

os.environ['CONFIG_FILE'] = "/etc/.ml-task-fusion/main.conf"
queue_cli = queue_client(queue_name=VllmModel().queue_name)

prompt = """
OCR the text of the image. Extract the text of the following fields and put it in a JSON format: 'why choose us', 'about us', 'company profile'. 

If the 'why choose us', 'about us', 'company profile' fields do not appear in the image, simply return [].

Ignore Other: Ignore all other text information in the picture except for the above fields.

IMPORTANT: 
    1. YOU MUST RESPOND ONLY WITH VALID JSON. DO NOT INCLUDE ANY INTRODUCTION, EXPLANATION, OR EXTRA TEXT. ONLY PROVIDE THE JSON ARRAY.
    2. NO ADDITIONAL TEXT.

Output format:
    [
        {
            "field": "field name 1",
            "sections": [
                {
                    "title": "",
                    "content": "chunk1 text here"
                },
                {
                    "title": "",
                    "content": "chunk2 text here"
                }
            ]
        },
        {
            "field": "field name 2",
            "sections": [
                {
                    "title": "",
                    "content": "chunk3 text here"
                },
                {
                    "title": "",
                    "content": "chunk4 text here"
                }
            ]
        }
    ]                    
"""
data = VllmData(prompt=prompt, images=[], max_tokens=1024, id=helper.unique_id())
result = queue_cli.push_and_response(job=QueueJobModel(id=data.id, data=data.model_dump()), seconds=120)
print(result)
```
