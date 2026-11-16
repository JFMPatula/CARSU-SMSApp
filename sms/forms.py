import re
from django import forms


class SMSForm(forms.Form):
    recipients = forms.CharField(
        label="Phone number(s)",
        help_text="Separate multiple numbers with commas. Example: 09171234567",
        widget=forms.TextInput(attrs={"placeholder": "09171234567, 09181234567"}),
    )
    message = forms.CharField(
        max_length=480,
        widget=forms.Textarea(attrs={"rows": 4, "id": "msg"}),
    )

    def clean_recipients(self):
        numbers = [n.strip() for n in self.cleaned_data["recipients"].split(",") if n.strip()]
        pattern = re.compile(r"^(09\d{9}|\+639\d{9})$")
        if not numbers:
            raise forms.ValidationError("Enter at least one number.")
        cleaned = []
        for n in numbers:
            if not pattern.match(n):
                raise forms.ValidationError(f"Invalid PH mobile number: {n}")
            # Normalize to E.164 format, e.g. +639171234567
            cleaned.append("+63" + n[1:] if n.startswith("09") else n)
        return cleaned
