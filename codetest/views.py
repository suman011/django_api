from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from datetime import datetime
from rest_framework.test import APIView
from rest_framework.response import Response
from .models import Event, EmailTemplate, EmailLog

class SendEventEmails(APIView):
    def get(self, request):
        current_date = datetime.date.today()
        events_today = Event.objects.filter(event_date=current_date)

        for event in events_today:
            try:
                employee = event.employee
                event_type = event.event_type
                email_template = EmailTemplate.objects.get(event_type=event_type)
                template_content = email_template.template
                template_content = template_content.format(employee=employee)

                subject = f"Event Reminder: {event_type}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [employee.email]

                # Send email using send_mail function
                send_mail(subject, template_content, from_email, recipient_list)

                # Log email status
                EmailLog.objects.create(event=event, email_sent=True)

            except Exception as e:
                # Log error
                EmailLog.objects.create(event=event, email_sent=False, error_message=str(e))

        return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
