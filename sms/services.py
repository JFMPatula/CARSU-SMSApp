"""Thin wrapper around the SimGate API (sends SMS via your own Android phone)."""
import os

import requests

SIMGATE_ENDPOINT = "https://api.simgate.app/v1/sms/send"


def send_sms(number: str, message: str) -> dict:
    """Send one SMS. Returns {'ok': bool, 'status': str, 'id': str, 'error': str}."""
    api_key = os.getenv("SIMGATE_API_KEY")
    device_id = os.getenv("SIMGATE_DEVICE_ID")
    if not api_key:
        return {"ok": False, "status": "Failed", "id": "", "error": "SIMGATE_API_KEY is not set"}
    if not device_id:
        return {"ok": False, "status": "Failed", "id": "", "error": "SIMGATE_DEVICE_ID is not set"}

    try:
        response = requests.post(
            SIMGATE_ENDPOINT,
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
            json={"deviceId": device_id, "phoneNumber": number, "message": message},
            timeout=15,
        )
        data = response.json()
        if response.ok:
            return {
                "ok": True,
                "status": "queued" if data.get("queued") else "sent",
                "id": str(data.get("messageId", "")),
                "error": "",
            }
        return {
            "ok": False,
            "status": "Failed",
            "id": "",
            "error": data.get("message") or data.get("error") or f"HTTP {response.status_code}",
        }
    except requests.RequestException as exc:  # network problems, timeouts, etc.
        return {"ok": False, "status": "Failed", "id": "", "error": str(exc)}
    except ValueError as exc:  # non-JSON response
        return {"ok": False, "status": "Failed", "id": "", "error": f"Invalid response: {exc}"}
