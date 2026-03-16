def calculate_profit(deal):

    arv = deal.arv
    price = deal.price
    repair = deal.estimated_repair

    profit = arv - (price + repair)

    return profit


def score_deal(deal):

    profit = calculate_profit(deal)

    if profit > 70000:
        return "A+ Deal"

    if profit > 40000:
        return "Good Deal"

    if profit > 20000:
        return "Average"

    return "Low Margin"
