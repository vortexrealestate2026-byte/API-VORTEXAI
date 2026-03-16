import time

from app.pipelines.pipeline_manager import run_all_pipelines
from app.ai.deal_scoring_ai import score_deals
from app.ai.buyer_match_ai import match_buyers


while True:

    run_all_pipelines()
    score_deals()
    match_buyers()

    print("Cycle finished")

    time.sleep(1800)
