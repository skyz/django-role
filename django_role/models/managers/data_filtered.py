# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from tls_middleware.utils import get_user


class RoleBasedGuardedMixin(object):
    data_filter_on = ['id']

    def get_filtered_query_set(self):

        filters = None

        user = get_user()
        qs = super(RoleBasedGuardedMixin, self).get_queryset()
        data_filter_on = self.data_filter_on
        model = self.model
        if not user:
            # If no user, return full qs (especially request has no user like celery vs. case)
            return qs

        if user.is_anonymous:
            return qs.none()

        if user.is_superuser:
            return qs

        # If user has data-filtering = false,return full qs
        if user:
            role = user.userrole_set.get().role
            if not role.status:
                return qs

            if not isinstance(data_filter_on, list):
                data_filter_on = list(data_filter_on)

            for data_filter_on_item in data_filter_on:
                field_names = data_filter_on_item.split('__')

                data_filter_key = []

                for field_name in field_names:
                    field = model._meta.get_field(field_name)

                    data_filter_key.append(field_name)

                    if hasattr(field, 'rel') and hasattr(field.rel, 'to'):
                        model = field.rel.to

                    model_name = model._meta.model_name

                    # get descended roles
                    descendants = role.get_descendants(include_self=True)

                    # get group perms
                    perms = list(descendants.filter(
                        groups__groupobjectpermission__permission__content_type__app_label=model._meta.app_label,
                        groups__groupobjectpermission__permission__content_type__model=model_name,
                        groups__groupobjectpermission__permission__codename='list_%s' % model_name).values_list(
                        'groups__groupobjectpermission__object_pk', flat=True))

                    # add role perms
                    perms += list(descendants.filter(
                        roleobjectpermission__permission__content_type__app_label=model._meta.app_label,
                        roleobjectpermission__permission__content_type__model=model_name,
                        roleobjectpermission__permission__codename='list_%s' % model_name).values_list(
                        'roleobjectpermission__object_pk', flat=True))

                    # add user perms
                    perms += list(user.userobjectpermission_set.filter(
                        permission__content_type__app_label=model._meta.app_label,
                        permission__content_type__model=model_name,
                        permission__codename='list_%s' % model_name).values_list(
                        'object_pk', flat=True))

                    if perms:
                        key = '%s__pk__in' % '__'.join(data_filter_key) if data_filter_key != ['id'] else 'pk__in'

                        if filters:
                            filters |= Q(**{key: perms})
                        else:
                            filters = Q(**{key: perms})
            if filters:
                return qs.filter(filters)

        return qs.none()


class DataFilteredManager(RoleBasedGuardedMixin, models.Manager):
    def __init__(self, data_filter_on=None):
        super(DataFilteredManager, self).__init__()

        if data_filter_on:
            self.data_filter_on = data_filter_on

    def get_queryset(self):
        return super(DataFilteredManager, self).get_filtered_query_set()
