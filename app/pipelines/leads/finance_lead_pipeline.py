import requests

FINANCE_FORM_API = "https://yourplatform.com/api/finance-leads"


def fetch_finance_leads():

    response = requests.get(FINANCE_FORM_API)

    if response.status_code != 200:
        return []

    data = response.json()

    leads = []

    for lead in data:

        leads.append({
            "name": lead.get("name"),
            "phone": lead.get("phone"),
            "email": lead.get("email"),
            "vehicle_interest": lead.get("vehicle"),
            "credit_score": lead.get("credit_score"),
            "income": lead.get("income"),
            "source": "finance_application"
        })

    return leads


def run():
    leads = fetch_finance_leads()
    print("Finance leads:", leads)
