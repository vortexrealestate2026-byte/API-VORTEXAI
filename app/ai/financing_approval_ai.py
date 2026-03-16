def score_financing_application(application):

    score = 0

    if application["credit_score"] > 700:
        score += 40

    if application["income"] > 40000:
        score += 30

    if application["down_payment"] > 2000:
        score += 20

    if application["employment_years"] > 2:
        score += 10

    return score
