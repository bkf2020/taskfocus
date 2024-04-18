from django.forms import ModelForm, ValidationError
from .models import Task
from django.utils import timezone

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["info", "start_time", "end_time", "whitelist"]

class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["info", "start_time", "end_time", "whitelist", "completed"]
    def clean(self):
        cleaned_data = super().clean()
        end_time = cleaned_data.get("end_time")
        if end_time is not None and (end_time - timezone.now()).total_seconds() // 60 > 5:
            raise ValidationError("You cannot finish the task now. Only within the last five minutes")
        return cleaned_data