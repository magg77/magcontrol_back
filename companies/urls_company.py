from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views_company import CompanyAdminViewSet, CompanyViewSet

router = DefaultRouter()

router.register(r'companies/create-with-admin', CompanyAdminViewSet, basename='companies/create-with-admin') #crear empresa con usuario admin
router.register(r'companies', CompanyViewSet, basename='companies')

urlpatterns = [
    path('', include(router.urls))
]