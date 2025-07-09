from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views_company import CompanyViewSet

router = DefaultRouter()

router.register(r'create-company', CompanyViewSet, basename='create-company') #crear empresa con usuario admin

urlpatterns = [
    path('', include(router.urls))
]