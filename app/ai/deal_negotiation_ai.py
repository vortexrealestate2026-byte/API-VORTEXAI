def calculate_offer(price, repair_cost, arv):

    target_profit = 30000

    offer = arv - repair_cost - target_profit

    if offer > price:
        return price
    else:
        return offer
