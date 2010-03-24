from os import environ
if not 'DJANGO_SETTINGS_MODULE' in environ:
    environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import unittest

from mongoengine import *
from mongoengine.connection import _get_db
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404
from django.conf import settings

class ShorcutsTest(unittest.TestCase):

    def setUp(self):
        connect(db='mongoenginetest')
        self.db = _get_db()
        class Person(Document):
            name = StringField()
            age = IntField()
        self.Person = Person

    def test_get_or_440(self):
        """Ensure that get_or_440 works.
        """
        self.Person.drop_collection()
        test_person = self.Person(name='Test')
        test_person.save()
        t2 = get_object_or_404(self.Person, id=test_person.id)
        self.assertEqual(test_person.id, t2.id)
        self.assertRaises(Http404, get_object_or_404, self.Person, id="4ba90141142bb528b1000001")
        self.Person.drop_collection()

    def test_get_list_or_404(self):
        """Ensure that get_list_or_404 works.
        """
        self.Person.drop_collection()
        test_person = self.Person(name='Test')
        test_person.save()
        t2 = get_list_or_404(self.Person)
        self.assertEqual(len(t2), 1)
        self.Person.drop_collection()

if __name__ == '__main__':
    print settings.DATABASES['default']
    unittest.main()

