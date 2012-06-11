# -*- coding: utf-8 -*-
"""
Holds all the information relevant to the client (addresses for instance)
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

BASE_ADDRESS_TEMPLATE = \
_("""
Name: %(name)s
""")

ADDRESS_TEMPLATE = getattr(settings, 'SHOP_ADDRESS_TEMPLATE',
                           BASE_ADDRESS_TEMPLATE)

class Address(models.Model):
    user_shipping = models.OneToOneField(User, related_name='shipping_address',
                                         blank=True, null=True)
    user_billing = models.OneToOneField(User, related_name='billing_address',
                                        blank=True, null=True)

    name = models.CharField(_('Name'), max_length=255)
    zip_code = models.CharField(_('Zip Code'), max_length=20)

    class Meta(object):
        verbose_name = _('Address')
        verbose_name_plural = _("Addresses")
        app_label = 'simple'

    def __unicode__(self):
        return '%s (%s, %s)' % (self.name, self.zip_code, self.city)

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name))
                           for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

    def as_text(self):
        return ADDRESS_TEMPLATE % {
            'name': self.name,
        }