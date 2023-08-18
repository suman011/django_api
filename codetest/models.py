from django.db import models

class Event(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_date = models.DateField()

class Employee(models.Model):
    email = models.EmailField(unique=True)

class EmailTemplate(models.Model):
    event_type = models.CharField(max_length=50, unique=True)
    template = models.TextField()

class EmailLog(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
