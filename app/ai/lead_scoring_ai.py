def score_lead(lead):

    score = 0

    if lead["credit_score"] > 650:
        score += 40

    if lead["income"] > 35000:
        score += 30

    if lead["down_payment"] > 1000:
        score += 20

    if lead["employment_years"] > 1:
        score += 10

    return score
