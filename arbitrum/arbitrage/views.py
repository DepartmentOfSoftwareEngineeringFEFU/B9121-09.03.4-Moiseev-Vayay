from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth.models import User
from arbitrage.models import UserTariff
from django.contrib.auth import get_user_model
from brokers.models import Tariff
from arbitrage_situation.models import ArbitrageOpportunity


#logins
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import RegisterForm

#tinkoff
from brokers.tink_api import get_price_by_figi
from brokers.tink_api import generate_price_chart

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'registration/login.html', {'error': 'Неверные данные'})

    return render(request, 'registration/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            exchanges = form.cleaned_data.get("exchanges")
            user.exchanges.set(exchanges)

            # сохраняем тарифы пользователя
            for exchange in exchanges:
                tariff_field = f'tariff_{exchange.id}'
                tariff = form.cleaned_data.get(tariff_field)
                if tariff:
                    UserTariff.objects.update_or_create(
                        user=user,
                        exchange=exchange,
                        defaults={"tariff": tariff}
                    )
            return redirect('login')
        else:
            print("❌ Ошибка регистрации:")
            print(form.errors)  # логируем ошибки в консоль
            return render(request, 'registration/register.html', {'form': form, 'errors': form.errors})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def tariff_list_api(request):
    exchange_id = request.GET.get("exchange_id")
    if not exchange_id:
        return JsonResponse({"error": "exchange_id required"}, status=400)

    tariffs = Tariff.objects.filter(exchange_id=exchange_id)
    data = [
        {"id": t.id, "name": t.name, "commission": float(t.commission)}
        for t in tariffs
    ]
    return JsonResponse(data, safe=False)



@login_required
def profile_view(request):
    price = get_price_by_figi("BBG004730N88")  # н USD/RUB
    usd_chart = generate_price_chart("BBG004730N88") 
    user_tariffs = UserTariff.objects.filter(user=request.user)
    commissions = {
        t.exchange.code: float(t.tariff.commission)
        for t in user_tariffs
    }
    arbitrages = ArbitrageOpportunity.objects.filter(is_active=True).order_by("-updated_at")
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'commissions': commissions,
        'usd_price': price,
        'usd_chart': usd_chart,
        'arbitrage_opportunities': arbitrages
    })

def logout_view(request):
    logout(request)
    return redirect('login')
# сохраняем выбранные биржи при регистрации 
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             exchanges = form.cleaned_data.get("exchanges")
#             user.exchanges.set(exchanges)  
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'registration/register.html', {'form': form})