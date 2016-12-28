from django import forms

class SimpleRequestForm(forms.Form):
    email = forms.EmailField()

    def get_user(self):
        from models import User
        try:
            return User.objects.get(email=self.cleaned_data['email'])
        except User.objects.DoesNotExist:
            return None

    def get_email(self):
        return self.cleaned_data['email']
