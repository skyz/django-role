# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from tls_middleware.utils import get_user

from django_role.models import Role


class UserRole(models.Model):
    role = models.ForeignKey(Role, verbose_name=_('Role'), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.CharField(max_length=100, blank=True, editable=False, null=True)
    updated_by = models.CharField(max_length=255, blank=True, editable=False, null=True)

    def save(self, **kwargs):
        user = get_user()
        self.updated_at = timezone.now()
        if user:
            self.updated_by = user.username if user else None
        if not self.pk:
            self.created_at = timezone.now()
            self.updated_at = self.created_at
            if user:
                self.created_by = user.username if user else None

        super(UserRole, self).save(**kwargs)

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')
