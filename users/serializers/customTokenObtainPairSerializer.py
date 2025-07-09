from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerialier(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        attrs[self.username_field] = attrs[self.username_field].lower() # normaliza el email
        return super().validate(attrs)