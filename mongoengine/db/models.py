#Django Facade

from mongoengine import StringField
from mongoengine import Document as Model
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import DecimalField
from mongoengine import DateTimeField as DateField
from mongoengine import ReferenceField as ForeignKey
from mongoengine import BooleanField
from mongoengine import IntField as IntegerField
from mongoengine import FloatField
from mongoengine import EmbeddedDocumentField
from mongoengine import EmbeddedDocument
from mongoengine import ListField
from mongoengine import DictField
from django.conf import settings

class CharField(StringField):
    """A unicode string field.
    """

    def __init__(self, help=None, **kwargs):
        super(CharField, self).__init__(**kwargs)

TextField = CharField
