from django.db import models


class SentMessage(models.Model):
    """Log of every SMS the app tries to send."""
    recipient = models.CharField(max_length=20)
    body = models.TextField(max_length=480)
    status = models.CharField(max_length=30, default="Pending")
    provider_message_id = models.CharField(max_length=50, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient} - {self.status}"
