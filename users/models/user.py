from django.db import models
from commons.models import TimeStampedModel

from django.contrib.auth.models import (
    BaseUserManager,         # Clase que define cómo se crean usuarios
    AbstractBaseUser,        # Clase base que gestiona contraseñas (hash, verificación, etc.)
    PermissionsMixin,        # Añade soporte para permisos y grupos
    Group,                   # Modelo de Django para agrupar usuarios
    Permission,              # Modelo que representa permisos individuales
)
from django.utils import timezone
from django.utils.timezone import localtime

from companies.models import Company
from commons.utils.validators import validate_user_company


# ---------- Constantes globales ---------- #

# Mapeo explícito entre rol y nombre de grupo
# Mapeo de rol -> nombre exacto del grupo en la base de datos
ROL_GRUPO_MAP = {
    'admin': 'Administradores',
    'cajero': 'Cajeros',
    'cliente': 'Clientes',
    'proveedor': 'Proveedores'
}

# Opciones válidas de rol (valor interno, etiqueta legible)
ROLES = (
    ('admin', 'Administrador'),
    ('cajero', 'Cajero'),
    ('cliente', 'Cliente'),
    ('proveedor', 'Proveedor')
)
        
# ---------- Manager personalizado ---------- #
class UserManager(BaseUserManager):
    
    #Crea un usuario regular. Es llamado cuando haces User.objects.create_user(...)    
    def create_user(self, identification_number, email, username, rol, company, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        if rol not in ROL_GRUPO_MAP:
            raise ValueError(f"Rol '{rol}' no es válido. Debe ser uno de: {', '.join(ROL_GRUPO_MAP.keys())}")
        if not company and not extra_fields.get('is_superuser', False):
            raise ValueError("El usuario debe tener una empresa asignada.")

        email = self.normalize_email(email).lower() # Limpia el correo (ej: convierte MAYÚSCULAS a minúsculas)
        
        # Crea la instancia del usuario
        user = self.model(
            identification_number=identification_number,
            email=email,
            username=username,
            rol=rol,
            company=company,
            **extra_fields
        ) 
        user.set_password(password) # Hashea la contraseña
        
        user.save(using=self._db) # Guarda el usuario en la base de datos configurada
           
        # Agregar grupo automáticamente según rol
        grupo_nombre = ROL_GRUPO_MAP[rol]
        try:
            grupo = Group.objects.get(name=grupo_nombre)
            user.groups.add(grupo)
        except Group.DoesNotExist:
            print(f"⚠️ Grupo '{grupo_nombre}' no encontrado en la base de datos.")
            
        # user = MyModel.objects.get(id=1)  # o el objeto que estés usando
        #print("guardado: ", localtime(user.date_joined))
        #print("update:", localtime(user.updated_at))
 
        return user
    
    #Crea un usuario administrador, llamado cuando haces createsuperuser. Se requiere para usar el panel de admin
    def create_superuser(self, email, username, password, **extra_fields):
        
        #Company = apps.get_model('users', 'Company')
        #default_company = Company.objects.last()
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        
        user = self.create_user(
            identification_number=extra_fields.get('identification_number', '0000000000'),  # 👈 Asignar uno por defecto o exigirlo
            email = self.normalize_email(email),
            username = username,
            rol='admin',
            company=None,  # superuser sin empresa
            **extra_fields
        )
        user.set_password(password)
        
        #validate_user_company(user)
                    
        user.save(using=self._db)
        return user
   
# ---------- Modelo personalizado ---------- #   
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    # AbstractBaseUser: gestiona la autenticación por contraseña, login-logout
    # PermissionsMixin: añade campos como is_superuser, groups y user_permissions
        
    identification_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,  # o False si quieres que sea obligatorio
        blank=True,  # o False si quieres que sea obligatorio
        verbose_name='Número de Identificación',
        help_text='Número único de identificación del usuario (cédula, NIT, etc.)'
    )    
    email = models.EmailField(unique=True) # Este será el identificador principal del usuario
    username = models.CharField(max_length=100) # Nombre del usuario
    rol = models.CharField(max_length=20, choices=ROLES) # Rol del usuario (tipo)
    is_active = models.BooleanField(default=True) # Si el usuario está activo
    is_staff = models.BooleanField(default=False) # Si puede acceder al panel de admin
    
    #date_joined = models.DateField(auto_now_add=True)
    date_joined = models.DateTimeField(default=timezone.now) # Fecha de creación
    updated_at = models.DateTimeField(default=timezone.now) # Fecha de última modificación
    
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,  # 👈 Permite NULL en base de datos
        blank=True, # 👈 No lo exige en formularios (como el createsuperuser)
        help_text='Empresa a la que pertenece el usuario. Solo el superusuario puede estar sin empresa.'
    )
       
    # Agrupa usuarios bajo permisos comunes
    # Se pueden asignar permisos a un grupo, y cualquier usuario dentro del grupo los hereda.
    # Ejemplo: grupo "cajeros" con permiso de "ver ventas".
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario',
        verbose_name='grupos'
    )
        
    # Permisos individuales    
    # Permite definir acciones específicas: añadir, editar, borrar, etc.
    # Este campo te permite asignar permisos individuales al usuario.
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Permisos específicos para este usuario',
        verbose_name='permisos de usuario'
    )
    
    objects = UserManager() # Establece el manager personalizado
    
    USERNAME_FIELD = 'email' # Le dice a Django que el campo principal de login será email, no username.
    #REQUIRED_FIELDS = ['username', 'company']
    REQUIRED_FIELDS = ['username']
    
    # se llama automaticamente con modelForm
    def clean(self):
        super().clean()
        validate_user_company(self)
    
    # Representación legible del usuario (útil para admin y debugging).
    def __str__(self):
        return f"{self.username} ({self.rol})"