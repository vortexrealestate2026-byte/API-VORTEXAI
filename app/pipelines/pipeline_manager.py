import logging
from datetime import datetime

# VEHICLE PIPELINES
from app.pipelines.vehicles.autotrader_pipeline import run as autotrader_pipeline
from app.pipelines.vehicles.cars_pipeline import run as cars_pipeline
from app.pipelines.vehicles.dealer_inventory_pipeline import run as dealer_inventory_pipeline
from app.pipelines.vehicles.tradein_pipeline import run as tradein_pipeline

# REAL ESTATE PIPELINES
from app.pipelines.real_estate.zillow_pipeline import run as zillow_pipeline
from app.pipelines.real_estate.redfin_pipeline import run as redfin_pipeline
from app.pipelines.real_estate.probate_pipeline import run as probate_pipeline
from app.pipelines.real_estate.tax_delinquent_pipeline import run as tax_pipeline
from app.pipelines.real_estate.vacant_property_pipeline import run as vacant_pipeline

# LEAD PIPELINES
from app.pipelines.leads.facebook_marketplace_pipeline import run as fb_marketplace_pipeline
from app.pipelines.leads.finance_lead_pipeline import run as finance_pipeline
from app.pipelines.leads.investor_network_pipeline import run as investor_pipeline
from app.pipelines.leads.referral_pipeline import run as referral_pipeline

# MARKETING PIPELINES
from app.pipelines.marketing.facebook_ads_pipeline import run as fb_ads_pipeline
from app.pipelines.marketing.google_ads_pipeline import run as google_ads_pipeline
from app.pipelines.marketing.tiktok_ads_pipeline import run as tiktok_ads_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def safe_run(pipeline, name):

    try:

        logging.info(f"Running pipeline: {name}")

        pipeline()

        logging.info(f"{name} finished")

    except Exception as e:

        logging.error(f"{name} FAILED: {e}")


def run_vehicle_pipelines():

    logging.info("Vehicle pipelines starting")

    safe_run(autotrader_pipeline, "Autotrader Pipeline")
    safe_run(cars_pipeline, "Cars Pipeline")
    safe_run(dealer_inventory_pipeline, "Dealer Inventory Pipeline")
    safe_run(tradein_pipeline, "Trade-in Pipeline")


def run_real_estate_pipelines():

    logging.info("Real estate pipelines starting")

    safe_run(zillow_pipeline, "Zillow Pipeline")
    safe_run(redfin_pipeline, "Redfin Pipeline")
    safe_run(probate_pipeline, "Probate Pipeline")
    safe_run(tax_pipeline, "Tax Delinquent Pipeline")
    safe_run(vacant_pipeline, "Vacant Property Pipeline")


def run_lead_pipelines():

    logging.info("Lead pipelines starting")

    safe_run(fb_marketplace_pipeline, "Facebook Marketplace Pipeline")
    safe_run(finance_pipeline, "Finance Lead Pipeline")
    safe_run(investor_pipeline, "Investor Network Pipeline")
    safe_run(referral_pipeline, "Referral Pipeline")


def run_marketing_pipelines():

    logging.info("Marketing pipelines starting")

    safe_run(fb_ads_pipeline, "Facebook Ads Pipeline")
    safe_run(google_ads_pipeline, "Google Ads Pipeline")
    safe_run(tiktok_ads_pipeline, "TikTok Ads Pipeline")


def run_all_pipelines():

    logging.info("========== STARTING ALL PIPELINES ==========")

    start_time = datetime.utcnow()

    run_vehicle_pipelines()
    run_real_estate_pipelines()
    run_lead_pipelines()
    run_marketing_pipelines()

    end_time = datetime.utcnow()

    runtime = end_time - start_time

    logging.info(f"========== PIPELINES FINISHED | Runtime: {runtime} ==========")


if __name__ == "__main__":

    run_all_pipelines()
