from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .services import update_user_roles, create_role
from .models import CustomUser, Role
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, RoleSerializer

class UserRoleViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Role.objects.all()

    def list(self, request):
        roles = self.get_queryset()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = create_role(serializer.validated_data)
        response_serializer = RoleSerializer(role)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def edit_role(self, request):
        user_id = request.data.get('user_id')
        role_ids = request.data.get('roles')

        if not user_id:
            raise ValidationError("user_id is required.")

        try:
            update_user_roles(user_id, role_ids)
            user = get_object_or_404(CustomUser.objects.all(), id=user_id)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)