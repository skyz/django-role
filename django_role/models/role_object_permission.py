# -*- coding: utf-8 -*-

from django.db import models
from guardian.models import BaseObjectPermission, BaseGenericObjectPermission

from django_role.models import Role
from django_role.models.managers.role_object_permission import RoleObjectPermissionManager


class RoleObjectPermissionBase(BaseObjectPermission):
    """
    **Manager**: :manager:`RoleObjectPermissionManager`
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = RoleObjectPermissionManager()

    class Meta:
        abstract = True
        unique_together = ['role', 'permission', 'content_object']


class RoleObjectPermission(RoleObjectPermissionBase, BaseGenericObjectPermission):
    class Meta:
        unique_together = ['role', 'permission', 'object_pk']
