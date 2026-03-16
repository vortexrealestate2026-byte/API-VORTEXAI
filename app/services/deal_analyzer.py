def score_deal(price, arv, repair_cost):

    mao = arv * 0.7 - repair_cost

    if price <= mao:
        return 90
    elif price <= mao * 1.1:
        return 70
    else:
        return 30
