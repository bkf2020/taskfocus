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

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

    def clean_website_regex(self):
        website_regex = self.cleaned_data.get('website_regex')
        print(self.pk)
        start_time = Task.objects.get(id=self.pk).start_time
        end_time = Task.objects.get(id=self.pk).end_time
        if end_time >= timezone.now() and timezone.now() >= start_time:
            raise ValidationError("You cannot add new whitelist websites")
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
        print(self.instance.task_id)
        start_time = Task.objects.get(id=self.instance.task_id).start_time
        end_time = Task.objects.get(id=self.instance.task_id).end_time
        if end_time >= timezone.now() and timezone.now() >= start_time:
            raise ValidationError("You cannot update whitelisted websites")
        validator_not_tld(website_regex)
        return website_regex
