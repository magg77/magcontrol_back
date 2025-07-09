from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (UserRegisterSerializer, UserSerializer, UserUpdateSerializer,
                               ChangePasswordSerializer, RequestPasswordResetSerializer, SetNewPasswordSerializer,)

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
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]  # si estás manejando sin autenticación
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_user_model().objects.get(email=email)

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/password-reset/{uidb64}/{token}"

        send_mail(
            subject="Restablecer contraseña de Magcontrol:",
            message=f"Da clic aquí para restablecer tu contraseña: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({'message': 'Se ha enviado un correo para restablecer la contraseña'}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]  # si estás manejando sin autenticación

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return Response({'error': 'Error al restablecer contraseña'}, status=status.HTTP_400_BAD_REQUEST)        