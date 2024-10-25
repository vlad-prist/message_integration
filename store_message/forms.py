from django import forms
from django.forms import BooleanField
from store_message.models import Store


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class StoreForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Store
        fields = '__all__'
        localized_fields = (
            'date_sanding',
            'date_receiving',
        )


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Яндекс Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
