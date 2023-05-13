from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FeedbackReport(models.Model):
    FEEDBACK = 'F'
    BUG_REPORT = 'B'
    HELP_REQUEST = 'H'
    SUBJECT_CHOICES = [
        (FEEDBACK, 'Feedback'),
        (BUG_REPORT, 'Reportar um bug'),
        (HELP_REQUEST, 'Preciso de ajuda')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=1, choices=SUBJECT_CHOICES)
    content = models.TextField()
