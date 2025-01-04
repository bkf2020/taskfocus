from django.forms import ModelForm, ValidationError
from .models import Task, WebsiteBlock
from django.utils import timezone

def validator_not_tld(website_regex):
    with open("tasks/tlds.txt", 'r') as f:
        for line in f:
            if website_regex.lower() == line.strip().lower():
                raise ValidationError("You can't submit a TLD!")

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["info", "start_time", "end_time", "whitelist"]

class WebsiteBlockForm(ModelForm):
    class Meta:
        model = WebsiteBlock
        fields = ["website_regex"]

    def clean_website_regex(self):
        website_regex = self.cleaned_data.get('website_regex')
        validator_not_tld(website_regex)
        return website_regex

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

class WebsiteBlockUpdateForm(ModelForm):
    class Meta:
        model = WebsiteBlock
        fields = ["website_regex"]

    def clean_website_regex(self):
        website_regex = self.cleaned_data.get('website_regex')
        validator_not_tld(website_regex)
        return website_regex
