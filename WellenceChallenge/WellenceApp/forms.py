from django import forms

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)



class TaskForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    email = forms.EmailField()
    task = forms.CharField(max_length=255)
    due_by = forms.DateTimeField()
    priority = forms.ChoiceField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')])
    is_urgent = forms.BooleanField(required=False)
