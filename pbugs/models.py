from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Reporter(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    first_use = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Issue(models.Model):
    #for issue kind
    UNA = "UA"
    BUG = "BUG"
    ENHANCEMENT = "ENHANCEMENT"
    kind_options = (
        (UNA, "Unassigned"),
        (BUG, "Bug"),
        (ENHANCEMENT, "Enhancement")
    )
    #for development stage
    DEV = "DEV"
    NOT_STARTED = "NOT_STARTED"
    DONE = "DONE"
    stage_options = (
        (DEV, "Under Dev"),
        (NOT_STARTED, "Not started"),
        (DONE, "resolved")
    )
    #for criticality level
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NOD = "ND"
    crictical_options = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (NOD, "Not determined")
    )
    #for platform
    WEB = "WEB"
    ANDROID = "ANDROID"
    PLATESBUGS = "PLATESBUGS"
    platform_options = (
        (WEB, "platestheapp.com"),
        (ANDROID, "Android"),
        (PLATESBUGS, "Plates Bugs")
    )
    reporter = models.ForeignKey(
        Reporter,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    kind = models.CharField(max_length=15, choices=kind_options, default='UA')
    stage = models.CharField(max_length=50, choices=stage_options, default='NOT_STARTED')
    criticality = models.CharField(max_length=50, choices=crictical_options, default="ND")
    platform = models.CharField(max_length=20, choices=platform_options, default="ANDROID")
    create_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    reporter = models.ForeignKey(
        Reporter,
        on_delete=models.CASCADE)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text
