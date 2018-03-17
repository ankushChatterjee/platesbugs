from django import forms
from .models import *
from django_markdown.widgets import MarkdownWidget
from django.contrib.auth.models import User

class PasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'platform']

class CommentForm(forms.Form):
    text = forms.CharField(label='Your Comment', widget=forms.Textarea)

class IssueEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['kind', 'stage', 'criticality']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter
        fields = ['is_admin']