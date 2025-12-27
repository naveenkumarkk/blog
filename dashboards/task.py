from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.db import transaction
from blogs.models import NewsLetter,NewsLetterUser,NewsLetterMail
import markdown

def send_newsletter_email(newsletter_id):
    newsletter = get_object_or_404(NewsLetter, id=newsletter_id)

    if newsletter.status == "Sent":
        return "Already sent"

    subscribers = NewsLetterUser.objects.filter(status="Subscribed")

    if not subscribers.exists():
        return "No subscribers"

    # Convert markdown to HTML
    html_body = markdown.markdown(
        newsletter.body,
        extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"]
    )

    success_count = 0
    failure_count = 0

    for subscriber in subscribers:
        mail_log, created = NewsLetterMail.objects.get_or_create(
            newsletter=newsletter,
            subscriber=subscriber,
            defaults={"status": "Pending"},
        )

        if not created and mail_log.status == "Success":
            continue 

        try:
            # Create email with HTML alternative
            msg = EmailMultiAlternatives(
                subject=newsletter.subject,
                body=newsletter.body,  # Plain text fallback
                from_email="naveenkumar.dev.io@gmail.com",
                to=[subscriber.email]
            )
            # Attach HTML version
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)

            mail_log.status = "Success"
            mail_log.save()
            success_count += 1

        except Exception:
            mail_log.status = "Failed"
            mail_log.save()
            failure_count += 1

    newsletter.status = "Sent"
    newsletter.save()

    return f"Sent: {success_count}, Failed: {failure_count}"
