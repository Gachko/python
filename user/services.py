from django.shortcuts import get_object_or_404
from .models import CustomUser, Role
from rest_framework.exceptions import ValidationError

def update_user_roles(user_id, role_ids):
    user = get_object_or_404(CustomUser, id=user_id)
    roles = Role.objects.filter(id__in=role_ids)

    user.roles.set(roles)
    user.save()


def create_role(data):
    return Role.objects.create(**data)