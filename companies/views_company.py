from rest_framework import viewsets
from .models import Company
from .serializer_company import CompanyAdminSerializer, CompanySerializer
from rest_framework.permissions import AllowAny

class CompanyAdminViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.none()
    serializer_class = CompanyAdminSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']    #solo permitir post
    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    
     