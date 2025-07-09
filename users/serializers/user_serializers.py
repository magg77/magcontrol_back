from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

# register user
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=6)
        
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'rol', 'password', 'company']
    
    def validate(self, data):
        company = data.get('company')
        rol = data.get('rol')
        
        if not company:
            raise serializers.ValidationError("La empresa es requerida para este tipo de usuario.")
        
        if rol == 'admin':
            exists_admin = User.objects.filter(company=company, rol='admin').exists()
            if exists_admin:
                raise serializers.ValidationError("Ya existe un usuario administrador para esta empresa")
            
        return data    
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User.objects.create_user(password=password, **validated_data)
        return user    

        
# get profile       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'rol']


# create company with user admin
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'rol', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'rol': {'default': 'admin'}
        }
        
    def validate_email(self, value):
        return value.lower()    
        
    def validate_rol(self, value):
        if value != 'admin':
            raise serializers.ValidationError("Solo se permite rol 'admin' al crear una empresa.")
        return value
    
    def validate(self, data):
        email = data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo electrónico.")
        return data

       
# update user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'rol', 'company', 'is_active']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'rol': {'required': False},
            'company': {'required': False},
        }
    
    def validate(self, attrs):
        instance = self.instance
        if instance and not instance.is_superuser:
            if not attrs.get('company') and not instance.company:
                raise serializers.ValidationError("El usuario debe estar asociado a una empresa.")
        return attrs    


# change password user
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)


# recovery password   