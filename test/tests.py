from __future__ import unicode_literals

from pendulum import Pendulum
from django.core import serializers
from django.test import TestCase
from django.utils import timezone

from django_pendulum_field.forms import PendulumField as PendulumFormField
from .forms import PersonForm
from .models import User, UserAutoNow, UserAutoNowAdd


class PendulumModelFieldTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='John',
            creation_date=Pendulum(2000, 6, 1, tzinfo='Europe/Berlin'),
        )

    def test_retrieved_model_returns_pendulum_instance(self):
        user = User.objects.get()
        self.assertTrue(isinstance(user.creation_date, Pendulum))
        self.assertEqual(user.creation_date, Pendulum(2000, 6, 1, tzinfo='Europe/Berlin'))

    def test_pendulum_instance_can_be_set_to_model_field(self):
        user = User.objects.get()
        user.creation_date = Pendulum(1990, 6, 1, tzinfo='Europe/Berlin')
        user.save()
        self.assertEqual(user.creation_date, Pendulum(1990, 6, 1, tzinfo='Europe/Berlin'))

    def test_parse_datetime_string(self):
        user = User.objects.get()
        user.creation_date = '2010-07-01'
        user.full_clean()
        user.save()
        self.assertTrue(isinstance(user.creation_date, Pendulum))
        self.assertEqual(user.creation_date, Pendulum(2010, 7, 1, tzinfo=timezone.get_current_timezone()))

    def test_parse_iso8601_string(self):
        user = User.objects.get()
        user.creation_date = '2010-07-01T00:00:00-10:00'
        user.full_clean()
        user.save()
        self.assertTrue(isinstance(user.creation_date, Pendulum))
        self.assertEqual(user.creation_date, Pendulum(2010, 7, 1, tzinfo='US/Hawaii'))

    def test_auto_now_works_correctly(self):
        user = UserAutoNow(first_name='James')
        user.save()
        self.assertTrue(isinstance(user.creation_date, Pendulum))

        first_creation_date = user.creation_date

        user.save()

        self.assertGreater(user.creation_date, first_creation_date)

    def test_auto_now_add_works_correctly(self):
        user = UserAutoNowAdd(first_name='Jason')
        user.save()
        self.assertTrue(isinstance(user.creation_date, Pendulum))

        first_creation_date = user.creation_date

        user.save()

        self.assertEqual(user.creation_date, first_creation_date)

    def test_field_lookups_work_correctly(self):
        self.assertEqual(
            User.objects.filter(creation_date__gt=Pendulum(1990, 6, 1, tzinfo='Europe/Berlin')).count(),
            1
        )

        self.assertEqual(
            User.objects.filter(creation_date__lt=Pendulum(1990, 6, 1, tzinfo='Europe/Berlin')).count(),
            0
        )

        self.assertEqual(
            User.objects.filter(creation_date__lt=Pendulum(2010, 6, 1, tzinfo='Europe/Berlin')).count(),
            1
        )

        self.assertEqual(
            User.objects.filter(creation_date__year=2000).count(),
            1
        )

        self.assertEqual(
            User.objects.filter(creation_date__year=2001).count(),
            0
        )

    def test_pendulumfield_serializes_correctly(self):
        data = serializers.serialize("json", User.objects.all())
        result = list(serializers.deserialize("json", data))
        self.assertEqual(result[0].object.creation_date, Pendulum(2000, 6, 1, tzinfo='Europe/Berlin'))


class PendulumFormFieldTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='John',
            creation_date=Pendulum(2000, 6, 1, tzinfo='Europe/Berlin'),
        )
        self.form = PersonForm(instance=self.user)

    def test_pendulum_form_field_automatically_used_on_modelform(self):
        self.assertEqual(self.form.fields['creation_date'].__class__, PendulumFormField)

    def test_form_renders_correctly(self):
        # should not raise Exception
        self.form.as_p()

    def test_form_strptime_works(self):
        # in case of no timezone given, it should use the current timezone
        datetime_string = Pendulum(2010, 5, 1).to_datetime_string()
        form = PersonForm({'first_name': 'Greg', 'creation_date': datetime_string}, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['creation_date'], Pendulum(2010, 5, 1,
                                                                               tzinfo=timezone.get_current_timezone()))

    def test_iso8601_form_field_works(self):
        iso8601_string = Pendulum(2010, 7, 1, tzinfo='US/Central').to_iso8601_string()
        form = PersonForm({'first_name': 'Greg', 'creation_date': iso8601_string}, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['creation_date'], Pendulum(2010, 7, 1, tzinfo='US/Central'))
