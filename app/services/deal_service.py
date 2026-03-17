from app.database import SessionLocal

def get_deals():
    db = SessionLocal()

    # placeholder data until database models are added
    deals = [
        {"address": "123 Main St", "price": 150000},
        {"address": "456 Oak Ave", "price": 200000}
    ]

    db.close()

    return {"deals": deals}
