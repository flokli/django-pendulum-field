# django-pendulum-field

Django Pendulum field is a custom model field wich stores datetimes in the database, but returns [pendulum](https://pendulum.eustace.io/) instances ("Handle datetimes, timedeltas and timezones in a more natural fashion.").

## Installation
```
pip install django-pendulum-field
```

## Usage
Simply add a PendulumField field to the model class:

```python
from django.db import models
from django_pendulum_field.fields import PendulumField


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    birthday = PendulumField()
```

And use it like you would normally do:

```python
import pendulum

person = Person.objects.create(
    first_name='Jacob',
    birthday=pendulum.Pendulum(1994, 11, 7, tzinfo='America/Vancouver')
)

person.birthday
# TODO

person = Person.objects.get(birthday=pendulum.Pendulum(1994, 11, 7, tzinfo='America/Vancouver'))
person.first_name
# Jacob
```

## Known issues
Doesn't work with Django 1.9 (1.8 and >= 1.10 work) (see [bugreport](https://code.djangoproject.com/ticket/27544))
