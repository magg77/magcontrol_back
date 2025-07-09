from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer, ChangePasswordSerializer

User = get_user_model()

# register user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]    
  
# get profile    
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

#close session      
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Token de actualización requerido."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# update user
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # o 'id' si lo prefieres explícitamente


# change password user
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(current_password):
                return Response({"current_password": "Contraseña actual incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# recovery password        
        