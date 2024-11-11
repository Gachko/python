from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRoleViewSet

router = DefaultRouter()
router.register(r'roles', UserRoleViewSet, basename='user-roles')

urlpatterns = [
    path('', include(router.urls)),
]