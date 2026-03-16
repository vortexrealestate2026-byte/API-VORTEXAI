def send_sms(phone: str, message: str):

    try:

        print(f"Sending SMS to {phone}")
        print(message)

        # later integrate Twilio or another SMS provider

    except Exception as e:

        print("SMS error:", e)
