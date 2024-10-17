import os
import argparse
import threading
from mltaskfusion.task import task_pipeline, task_names


def main():
    parser = argparse.ArgumentParser(description="Command line tool for model selection.")
    parser.add_argument("--config", type=str, required=True, help="配置文件")
    parser.add_argument("--models", type=str, required=True, help="模型名称，多个使用英文,分隔.")

    args = parser.parse_args()
    models = [model for model in args.models.split(",") if model in task_names]

    os.environ["CONFIG_FILE"] = args.config
    threads = []

    for model in models:
        thread = threading.Thread(target=task_pipeline, args=(model,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
