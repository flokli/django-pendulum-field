import datetime

import pendulum
from django.core import exceptions
from django.forms import DateTimeField
from django.utils import timezone
from pendulum import Pendulum
from pendulum.parsing.exceptions import ParserError


class PendulumField(DateTimeField):
    def prepare_value(self, value):
        return value.to_datetime_string()

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
            return pendulum.parse(value, tz=timezone.get_current_timezone())
        except ParserError:
            raise exceptions.ValidationError(
                self.error_messages['invalid_datetime'],
                code='invalid_datetime',
                params={'value': value},
            )

    def strptime(self, value, format):
        return pendulum.from_format(value, format, timezone.get_current_timezone())
