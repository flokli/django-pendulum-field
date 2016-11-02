import datetime

import pendulum
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pendulum import Pendulum
from pendulum.parsing.exceptions import ParserError

from django_pendulum_field import forms


class PendulumField(models.DateTimeField):
    """
    A date and time, including timezone information, represented in Python by a `pendulum.Pendulum` object.
    """

    description = _("A date and time, including timezone information")

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return pendulum.Pendulum.instance(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, Pendulum):
            return value
        if isinstance(value, datetime.datetime):
            return Pendulum.instance(value)
        if isinstance(value, datetime.date):
            return Pendulum.instance(datetime.datetime.combine(value, datetime.datetime.min.time()))

        try:
            return pendulum.parse(value)
        except ParserError:
            raise exceptions.ValidationError(
                self.error_messages['invalid_datetime'],
                code='invalid_datetime',
                params={'value': value},
            )

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return '' if value is None else value.isoformat()

    def pre_save(self, model_instance, add):
        value = super(PendulumField, self).pre_save(model_instance, add)
        if isinstance(value, datetime.datetime):
            value = pendulum.Pendulum.instance(value)
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.PendulumField}
        defaults.update(kwargs)
        return super(PendulumField, self).formfield(**defaults)
