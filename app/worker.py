import time
import logging

from app.pipelines.pipeline_manager import run_all_pipelines


logging.basicConfig(level=logging.INFO)


def start_worker():

    while True:

        logging.info("Starting pipeline cycle")

        run_all_pipelines()

        logging.info("Sleeping 30 minutes")

        time.sleep(1800)


if __name__ == "__main__":
    start_worker()
