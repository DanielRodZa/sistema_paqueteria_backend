from django.db import models
from django.contrib.auth.models import AbstractUser

from sucursales.models import Sucursal


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        RECEPCIONISTA = "RECEPCIONISTA", "Recepcionista"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RECEPCIONISTA)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.username: # Only generate on creation if username is empty
             self.generate_username()
        super().save(*args, **kwargs)

    def generate_username(self):
        import unicodedata
        import re

        def sanitize(text):
            if not text: return ""
            # Normalize unicode characters to removing accents
            nfkd_form = unicodedata.normalize('NFKD', text)
            only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
            # Remove non-alphanumeric and uppercase
            return re.sub(r'[^A-Z0-9]', '', only_ascii.upper())

        # 1. Role (3 letters)
        role_part = self.role[:3].upper() if self.role else 'USR'

        # 2. Sucursal (4 digits/chars)
        if self.sucursal:
            try:
                # Assuming sucursal.id is like SUC1, we might want to just take the ID string 
                # but formatted to 4 chars. If it's "SUC1", it fits.
                # If we want purely digits from SUC1 -> 0001, we'd need parsing.
                # Requirement says "4 digits of sucursal". Assuming SUC ID is the reference.
                # Let's clean it to be safe or just take the ID.
                suc_part = self.sucursal.id[-4:].upper().zfill(4) 
            except:
                suc_part = '0000'
        else:
            suc_part = '0000'

        # 3. Name (3 letters)
        name_sanitized = sanitize(self.first_name)
        name_part = name_sanitized[:3] if name_sanitized else 'XXX'

        # 4. Last Name (3 letters)
        last_sanitized = sanitize(self.last_name)
        last_part = last_sanitized[:3] if last_sanitized else 'XXX'

        base_username = f"{role_part}-{suc_part}-{name_part}{last_part}"
        
        # Check uniqueness
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        self.username = username