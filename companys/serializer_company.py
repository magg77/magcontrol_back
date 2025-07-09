from rest_framework import serializers
from companys.models_company import Company
from users.models import User
from users.serializers.user_serializers import AdminUserSerializer

class CompanySerializer(serializers.ModelSerializer):
    admin = AdminUserSerializer(write_only = True)
    
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'nit', 'address', 'cell', 'phone', 'email', 'admin']
        
    def validate_email_company(self, value):
        value = value.lower()
        if Company.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe una empresa registrada con este correo.")
        return value
        
    def validate_user(self, data):
        admin_data = data.get('admin')

        if not admin_data:
            raise serializers.ValidationError("Los datos del administrador son requeridos.")

        # Validar que no exista otro admin con ese email
        email = admin_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email.")

        return data    
        
    def create(self, validate_data):
        admin_data = validate_data.pop('admin')
        
        # crear la empresa
        company = Company.objects.create(**validate_data)
        
        #crear el usuario admin asociado a la empresa
        admin_user = User.objects.create_user(
            email = admin_data['email'],
            username = admin_data['username'],
            password = admin_data['password'],
            rol=admin_data.get('rol', 'admin'),  # ✅ Se extrae de admin_data o default 'admin'
            company = company
        )
        
        return company