#Django Facade
from mongoengine import Document as Model
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import DateTimeField as DateField
from mongoengine import ReferenceField as ForeignKey
from mongoengine import BooleanField, DecimalField
from mongoengine import IntField as IntegerField
from mongoengine import DecimalField as FloatField

from mongoengine import ListField
from django.conf import settings

dir(settings)

class CharField(StringField):
    """A unicode string field.
    """

    def __init__(self, help=None, **kwargs):
        super(CharField, self).__init__(**kwargs)

TextField = CharField
