import os
import django
from django.contrib.auth import get_user_model

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paqueteria_api.settings")
django.setup()

def create_superuser():
    User = get_user_model()
    
    # Obtener credenciales de variables de entorno
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not username or not password:
        print("Error: Las variables DJANGO_SUPERUSER_USERNAME y DJANGO_SUPERUSER_PASSWORD son requeridas.")
        return

    if not User.objects.filter(username=username).exists():
        print(f"Creando superusuario '{username}'...")
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"¡Superusuario '{username}' creado exitosamente!")
        except Exception as e:
            print(f"Error al crear superusuario: {e}")
    else:
        print(f"El superusuario '{username}' ya existe.")

if __name__ == "__main__":
    create_superuser()
