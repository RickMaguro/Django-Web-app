from django import forms

# class TaskForm(forms.Form):
#     task = forms.CharField(max_length=255)
#     due_by = forms.DateTimeField()
#     priority = forms.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
#     is_urgent = forms.BooleanField(default=False)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)