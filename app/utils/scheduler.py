import time
from app.pipelines.pipeline_manager import run_all_pipelines
from app.ai.deal_scoring_ai import score_deals
from app.agents.deal_distribution_agent import distribute_deals


def start_scheduler():

    while True:

        print("Running pipelines")
        run_all_pipelines()

        print("Running AI scoring")
        score_deals()

        print("Distributing deals")
        distribute_deals()

        time.sleep(1800)
