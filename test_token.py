import os
import sys
import django
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

# Configurar Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paqueteria_api.settings')
django.setup()

User = get_user_model()

def test_superuser_token():
    try:
        # Buscar un superusuario
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            print("No superuser found.")
            return

        print(f"Testing token for superuser: {superuser.username}")
        print(f"Superuser DB Role: {superuser.role}")

        # Generar token manualmente (como lo hace la vista)
        from users.serializers import MyTokenObtainPairSerializer
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(superuser)

        print(f"Token Role Claim: {token.get('role')}")
        
        # Probar la respuesta completa (validate method)
        # Necesitamos simular los atributos que espera validate
        serializer.user = superuser
        data = serializer.validate({})
        print(f"Response Data Role: {data.get('role')}")
        print(f"Response Data Username: {data.get('username')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_superuser_token()
