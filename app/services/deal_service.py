def get_deals():
    """
    Temporary mock deals.
    Eventually this will pull from a database.
    """

    deals = [
        {
            "id": 1,
            "vehicle": "2022 BMW M3",
            "price": 72000,
            "mileage": 15000
        },
        {
            "id": 2,
            "vehicle": "2021 Tesla Model S",
            "price": 68000,
            "mileage": 12000
        },
        {
            "id": 3,
            "vehicle": "2023 Porsche 911",
            "price": 132000,
            "mileage": 5000
        }
    ]

    return deals
