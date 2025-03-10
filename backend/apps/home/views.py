from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
import json

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

def home_view(request):
    endpoints = [
        {"name": "Películas", "url": "/movies"},
        {"name": "Búsqueda de una película (search: Love)", "url": "/movies?search=Love"},
        {"name": "Detalle de una película (id: 1)", "url": "/movies/1"},
        {"name": "Accede al frontend anterior", "url": "/movies/old"}
    ]
    return render(request, "home.html", {"endpoints": endpoints})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Guarda el usuario y lo autentica automáticamente"""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login exitoso",
                                 'username': username}, status=200)
        else:
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout exitoso"}, status=200)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'El nombre de usuario y la contraseña son obligatorios'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

            # Crear usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'message': 'Usuario registrado con éxito',
                                 'username': username}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método de solicitud no válido'}, status=405)
