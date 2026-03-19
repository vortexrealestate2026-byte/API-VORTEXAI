import logging
from typing import Optional

import stripe
from sqlalchemy.orm import Session

from app.config import settings
from app.models.dealer import Dealer

logger = logging.getLogger("vortex.stripe")

stripe.api_key = settings.STRIPE_SECRET_KEY

METERED_PRODUCT_NAME = "VortexAI Car Leads"
METERED_PRICE_NICKNAME = "per_lead_cad"


class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_customer(self, dealer: Dealer) -> str:
        try:
            customer = stripe.Customer.create(
                email=dealer.email,
                name=dealer.company_name,
                metadata={
                    "dealer_id": str(dealer.id),
                    "province": dealer.province,
                },
            )
            logger.info(f"Stripe customer created for dealer {dealer.id}: {customer.id}")
            return customer.id
        except stripe.StripeError as exc:
            logger.error(f"Stripe create_customer error for dealer {dealer.id}: {exc}")
            raise

    def _get_or_create_metered_price(self, per_lead_rate_cents: int) -> str:
        products = stripe.Product.list(active=True, limit=100)
        product_id = None
        for p in products.auto_paging_iter():
            if p.name == METERED_PRODUCT_NAME:
                product_id = p.id
                break

        if not product_id:
            product = stripe.Product.create(name=METERED_PRODUCT_NAME)
            product_id = product.id

        prices = stripe.Price.list(product=product_id, active=True, limit=100)
        for price in prices.auto_paging_iter():
            if (
                price.recurring
                and price.recurring.usage_type == "metered"
                and price.unit_amount == per_lead_rate_cents
                and price.currency == "cad"
            ):
                return price.id

        price = stripe.Price.create(
            product=product_id,
            unit_amount=per_lead_rate_cents,
            currency="cad",
            recurring={"interval": "month", "usage_type": "metered"},
            nickname=METERED_PRICE_NICKNAME,
        )
        return price.id

    def create_metered_subscription(self, dealer: Dealer) -> str:
        per_lead_rate_cents = int(float(dealer.per_lead_rate) * 100)
        price_id = self._get_or_create_metered_price(per_lead_rate_cents)
        try:
            subscription = stripe.Subscription.create(
                customer=dealer.stripe_customer_id,
                items=[{"price": price_id}],
                metadata={"dealer_id": str(dealer.id)},
            )
            logger.info(f"Stripe subscription created for dealer {dealer.id}: {subscription.id}")
            return subscription.id
        except stripe.StripeError as exc:
            logger.error(f"Stripe create_metered_subscription error for dealer {dealer.id}: {exc}")
            raise

    def record_lead_usage(self, dealer: Dealer, quantity: int = 1) -> Optional[str]:
        if not dealer.stripe_subscription_id:
            logger.warning(f"Dealer {dealer.id} has no Stripe subscription, skipping usage record")
            return None
        try:
            subscription = stripe.Subscription.retrieve(dealer.stripe_subscription_id)
            subscription_item_id = subscription["items"]["data"][0]["id"]
            usage_record = stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=quantity,
                action="increment",
            )
            logger.info(f"Usage record created for dealer {dealer.id}: {usage_record.id}")
            return usage_record.id
        except stripe.StripeError as exc:
            logger.error(f"Stripe record_lead_usage error for dealer {dealer.id}: {exc}")
            return None

    def get_billing_summary(self, dealer: Dealer) -> dict:
        if not dealer.stripe_subscription_id:
            return {"error": "No subscription found", "usage": 0, "amount_due": 0}
        try:
            subscription = stripe.Subscription.retrieve(dealer.stripe_subscription_id)
            subscription_item_id = subscription["items"]["data"][0]["id"]
            usage_summary = stripe.SubscriptionItem.list_usage_record_summaries(
                subscription_item_id,
                limit=1,
            )
            total_usage = 0
            if usage_summary.data:
                total_usage = usage_summary.data[0].total_usage

            amount_due = total_usage * float(dealer.per_lead_rate)
            return {
                "dealer_id": str(dealer.id),
                "subscription_id": dealer.stripe_subscription_id,
                "current_period_usage": total_usage,
                "per_lead_rate_cad": float(dealer.per_lead_rate),
                "estimated_amount_due_cad": round(amount_due, 2),
            }
        except stripe.StripeError as exc:
            logger.error(f"Stripe get_billing_summary error for dealer {dealer.id}: {exc}")
            return {"error": str(exc)}
