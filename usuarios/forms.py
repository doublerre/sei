from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class UserForm(forms.ModelForm):
    repassword = forms.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'repassword')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-l',
                    'placeholder': 'Nombre de usuario'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-l',
                    'placeholder': 'Correo electrónico'
                }),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password(self, *args, **kwargs):
        if self.data['password'] != self.data['repassword']:
            raise forms.ValidationError(
                'Las contraseñas no coinciden.')

        return self.data['password']
