# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Role(MPTTModel):
    name = models.CharField(_('Role Name'), max_length=200, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name="children", verbose_name='Parent Role',
                            on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, verbose_name=_('Group'))

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.name
