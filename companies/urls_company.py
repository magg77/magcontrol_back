from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views_company import CompanyAdminViewSet, CompanyViewSet

router = DefaultRouter()

router.register(r'create-company', CompanyAdminViewSet, basename='create-company') #crear empresa con usuario admin
router.register(r'company', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls))
]