from rest_framework import viewsets
from .models_company import Company
from .serializer_company import CompanySerializer
from rest_framework.permissions import AllowAny

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.none()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']    #solo permitir post
     