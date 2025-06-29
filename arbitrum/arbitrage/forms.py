from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from brokers.models import Exchange
from brokers.models import Tariff
from arbitrage.models import UserTariff

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    passport_data = forms.CharField(max_length=20)
    balance = forms.DecimalField()
    
    exchanges = forms.ModelMultipleChoiceField(
        queryset=Exchange.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Где у вас есть аккаунт"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].required = False

        # динамически добавляем поля тарифов по каждой бирже
        for exchange in Exchange.objects.all():
            self.fields[f'tariff_{exchange.id}'] = forms.ModelChoiceField(
                queryset=Tariff.objects.filter(exchange=exchange),
                required=False,
                label=f'Тариф на {exchange.name}'
            )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'passport_data', 'balance', 'password1', 'password2', 'exchanges']

    def clean(self):
        cleaned_data = super().clean()
        selected_exchanges = cleaned_data.get("exchanges")

        for exchange in selected_exchanges:
            tariff_field = f"tariff_{exchange.id}"
            tariff = cleaned_data.get(tariff_field)
            if not tariff:
                self.add_error(tariff_field, f"Выберите тариф для биржи {exchange.name}")
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit)
        selected_exchanges = self.cleaned_data.get("exchanges")

        for exchange in selected_exchanges:
            tariff = self.cleaned_data.get(f"tariff_{exchange.id}")
            UserTariff.objects.create(
                user=user,
                exchange=exchange,
                tariff=tariff
            )

        return user