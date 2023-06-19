from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    """
    Signal sends email for password reset
    """

    email_plaintext_message = (
        f"{reverse('password_reset:reset-password-request')}"
        f"?token={reset_password_token.key}"
    )

    send_mail(
        "Password reset for export hunter",
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )
