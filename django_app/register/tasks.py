from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

@shared_task
def send_activation_email(user):
    path_ = reverse('activate', kwargs={"code": user.activation_key})
    #  TODO: prettify this
    full_path = f"http://0.0.0.0:8000{path_}"
    subject = 'Activate Account'
    from_email = settings.DEFAULT_FROM_EMAIL
    message = f'Activate your account here: {full_path}'
    recipient_list = [user.email]
    html_message = (
        f'<p>Follow the link to activate your account: {full_path}</p>'
    )
    print(html_message)
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        html_message=html_message,
    )