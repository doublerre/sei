from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import token_activacion
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
User = get_user_model()


# Create your views here.
class LoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        return super().form_invalid(form)


class RegistrarView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('usuarios:login')
    template_name = 'auth/registrar.html'
    success_message = "Un correo se le acaba de ser enviado para " + \
        "que pueda confirmar su correo electrónico, por favor verifiquelo " + \
        "para poder activar su cuenta. Recuerde revisar la carpeta de Spam"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        sitio = get_current_site(self.request)

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string(
            'confirmar_cuenta.html',
            {
                'user': user,
                'sitio': sitio,
                'uid': uid,
                'token': token
            }

        )

        mail_subject = 'Activar cuenta Sistema Estatal de" + \
        " Investigadores de Zacatecas'
        mail_to = user.email
        email = EmailMessage(
            mail_subject,
            mensaje,
            to=[mail_to],
        )

        email.content_subtype = 'html'
        email.send()

        return super().form_valid(form)


class ActivarCuentaView(TemplateView):

    def get(self, request, *args, **kwargs):

        try:
            uid = urlsafe_base64_decode(kwargs['uidb64'])
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None

        if (user is not None) and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Cuenta activada, ingresar datos")

        else:
            messages.error(
                request,
                "Error al activar la cuenta, contacta al administrador")

        return redirect('usuarios:login')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request),
                        'site_name': 'Sistema Estatal de Investigadores',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject, email, settings.EMAIL_HOST_USER,
                            [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            return redirect(reverse_lazy("password_reset_done"))
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="auth/password_reset.html",
        context={"password_reset_form": password_reset_form})
