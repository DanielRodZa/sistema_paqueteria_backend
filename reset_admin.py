import os
import django
from django.contrib.auth import get_user_model

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paqueteria_api.settings")
django.setup()

def reset_superuser():
    User = get_user_model()
    
    # Obtener credenciales de variables de entorno
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'loop_admin')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'LoopAdmin_5657')

    user = User.objects.filter(username=username).first()
    if user:
        print(f"Actualizando contraseña y rol para '{username}'...")
        user.set_password(password)
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"¡Contraseña y rol de '{username}' actualizados exitosamente!")
    else:
        print(f"El usuario '{username}' no existe. Creándolo...")
        user = User.objects.create_superuser(username=username, password=password)
        user.role = 'ADMIN'
        user.save()
        print(f"¡Superusuario '{username}' creado exitosamente con rol ADMIN!")

if __name__ == "__main__":
    reset_superuser()
