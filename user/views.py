from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .services import update_user_roles
from .models import CustomUser, Role
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer

class UserRoleViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def edit_role(self, request):
        user_id = request.data.get('user_id')
        role_ids = request.data.get('roles')

        if not user_id:
            raise ValidationError("user_id is required.")

        try:
            update_user_roles(user_id, role_ids)
            channels = CustomUser.objects.all()
            serializer = UserSerializer(channels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)