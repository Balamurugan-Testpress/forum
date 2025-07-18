from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter the text"}),
        max_length=4000,
        help_text="The max length of the text is 4000.",
    )

    class Meta:
        model = Topic
        fields = ["subject", "message"]
