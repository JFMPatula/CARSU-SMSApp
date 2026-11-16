# Django SMS Sender

IT 120 group assignment. A Django app that sends SMS through the SimGate API
(free SMS gateway using your own Android phone), supports multiple recipients,
validates PH numbers, and logs every message.

## Features

- Send to one or many recipients (comma-separated).
- Input validation with clear feedback (empty/invalid numbers, empty or
  over-long messages).
- Error handling for missing credentials, network failures, and provider
  rejections.
- **Live message preview** with a character counter and SMS-segment count.
- **SMS history / dashboard** at `/history/` with per-message status and errors.
- Credentials kept in `.env` (never committed); CSRF-protected forms.

## How it works

1. User opens the form, enters one or more numbers (comma-separated) and a message.
2. `SMSForm` validates the numbers and message length.
3. `views.send_view` loops through recipients and calls `services.send_sms`,
   which calls the SimGate REST API with `requests`.
4. Each attempt is saved as a `SentMessage` (status, error, timestamp).
5. `/history/` lists all sent messages and their status.

## Setup

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then put your SimGate API key and device ID in .env
python manage.py makemigrations sms
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## SimGate notes

SimGate sends SMS through **your own Android phone + SIM**, so messages cost
nothing extra (free plan: 250 messages/month, 10/day, 1 device). Setup:

1. Create an account at https://www.simgate.app (no credit card needed).
2. Install the **SimGate Gateway** app from Google Play on the phone with the
   SIM, then pair it by scanning the QR code in the dashboard.
3. In the dashboard, generate an **API key** and copy the phone's **Device ID**.
4. Put them in `.env` as `SIMGATE_API_KEY` and `SIMGATE_DEVICE_ID`.
5. Keep the phone online, charged, and set the app's battery usage to
   **Unrestricted** so it can send in the background.

The API returns `200` when the phone accepts the message and `202` when the
phone is briefly offline (the message is queued and retried automatically).
Numbers like 09171234567 are converted to +639171234567 automatically.

## Project wiring

- `settings.py`: add `"sms"` to `INSTALLED_APPS`, and at the top add
  `from dotenv import load_dotenv; load_dotenv()`
- project `urls.py`: `path("", include("sms.urls"))`

## Team

| Member                  | Responsibility                    |
| ----------------------- | --------------------------------- |
| Jean Faith Marie Patula | Backend (models, services, views) |
| Francine Claire Jamilo  | Frontend (templates, forms)       |
| Stanley James Apal      | README, testing, demo video       |
