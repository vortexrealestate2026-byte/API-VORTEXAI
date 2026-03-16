from app.models.deal import Deal
from app.models.buyer import Buyer


def match_buyers_to_deal(deal, buyers):

    matched = []

    for buyer in buyers:

        if buyer.city.lower() == deal.city.lower():
            matched.append(buyer)

    return matched


def send_deal_to_buyers(deal, buyers):

    matches = match_buyers_to_deal(deal, buyers)

    for buyer in matches:
        print(f"Sending deal {deal.title} to {buyer.email}")
