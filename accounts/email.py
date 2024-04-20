from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        
        user = context.get("user")
        context["uid"] = urlsafe_base64_encode(force_bytes(user.id))
        context["token"] = default_token_generator.make_token(user)
        context["url"] = 'activate/{uid}/{token}'.format(**context)
        return context


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        
        user = context.get("user")
        context["uid"] = urlsafe_base64_encode(force_bytes(user.id))
        context["token"] = default_token_generator.make_token(user)
        context["url"] = 'password-reset/{uid}/{token}'.format(**context)
        return context






