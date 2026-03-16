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


logging.basicConfig(level=logging.INFO)


def run_vehicle_pipelines():

    logging.info("Running vehicle pipelines")

    autotrader_pipeline()
    cars_pipeline()
    dealer_inventory_pipeline()
    tradein_pipeline()


def run_real_estate_pipelines():

    logging.info("Running real estate pipelines")

    zillow_pipeline()
    redfin_pipeline()
    probate_pipeline()
    tax_pipeline()
    vacant_pipeline()


def run_lead_pipelines():

    logging.info("Running lead pipelines")

    fb_marketplace_pipeline()
    finance_pipeline()
    investor_pipeline()
    referral_pipeline()


def run_marketing_pipelines():

    logging.info("Running marketing pipelines")

    fb_ads_pipeline()
    google_ads_pipeline()
    tiktok_ads_pipeline()


def run_all_pipelines():

    logging.info("Starting ALL pipelines")

    start_time = datetime.utcnow()

    run_vehicle_pipelines()
    run_real_estate_pipelines()
    run_lead_pipelines()
    run_marketing_pipelines()

    end_time = datetime.utcnow()

    logging.info(f"All pipelines finished. Runtime: {end_time - start_time}")


if __name__ == "__main__":
    run_all_pipelines()
