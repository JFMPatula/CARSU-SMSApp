from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SMSForm
from .models import SentMessage
from .services import send_sms


def send_view(request):
    form = SMSForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        body = form.cleaned_data["message"]
        sent = failed = 0
        for number in form.cleaned_data["recipients"]:
            result = send_sms(number, body)
            SentMessage.objects.create(
                recipient=number,
                body=body,
                status=result["status"],
                provider_message_id=result["id"],
                error=result["error"],
            )
            if result["ok"]:
                sent += 1
            else:
                failed += 1
        if sent:
            messages.success(request, f"{sent} message(s) sent.")
        if failed:
            messages.error(request, f"{failed} message(s) failed. See history.")
        return redirect("sms:send")
    return render(request, "sms/send.html", {"form": form})


def history_view(request):
    return render(request, "sms/history.html", {"items": SentMessage.objects.all()})
