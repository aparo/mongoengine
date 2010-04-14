from pymongo import Connection
from pymongo.son_manipulator import SONManipulator

try:
    from django.db.models import Model
    from django.contrib.contenttypes.models import ContentType
    
    def encode_django(model):
        if not model.pk:
            model.save()
        return {'app':model._meta.app_label, 
                'model':model._meta.module_name,
                'pk':model.pk,
                '_type':"django"}
    
    def decode_django(data):
        return ContentType.objects.get(app_label=data['app'], model=data['model']).get_object_for_this_type(pk=data['pk'])
    
    class TransformDjango(SONManipulator):
        def transform_incoming(self, son, collection):
            if isinstance(son, dict):
                for (key, value) in son.items():
                    if isinstance(value, Model):
                        son[key] = encode_django(value)
                    elif isinstance(value, dict): # Make sure we recurse into sub-docs
                        son[key] = self.transform_incoming(value, collection)
                    elif hasattr(value, "__iter__"): # Make sure we recurse into sub-docs
                        son[key] = [self.transform_incoming(item, collection) for item in value]
            elif hasattr(son, "__iter__"): # Make sure we recurse into sub-docs
                son = [self.transform_incoming(item, collection) for item in son]
            elif isinstance(son, Model):
                son = encode_django(value)
            return son
        
        def transform_outgoing(self, son, collection):
            if isinstance(son, dict):
                for (key, value) in son.items():
                    if isinstance(value, dict):
                        if "_type" in value and value["_type"] == "django":
                            son[key] = decode_django(value)
                    elif hasattr(value, "__iter__"): # Make sure we recurse into sub-docs
                        son[key] = [self.transform_outgoing(item, collection) for item in value]
                    else: # Again, make sure to recurse into sub-docs
                        son[key] = self.transform_outgoing(value, collection)
            elif hasattr(son, "__iter__"): # Make sure we recurse into sub-docs
                son = [self.transform_outgoing(item, collection) for item in son]
            elif isinstance(son, Model):
                son = decode_django(value)
            return son
except ImportError:
    #no django, disable SON
    TransformDjango = None

__all__ = ['ConnectionError', 'connect']

_connection_settings = {
    'host': 'localhost',
    'port': 27017,
}

_connection = None

_db_name = None
_db_username = None
_db_password = None
_db = None

try:
    from django.conf import settings
    for dbname in ['mongodb', 'default']:
        if dbname in settings.DATABASES:
            _connection_settings['host'] = settings.DATABASES[dbname]['HOST']
            port = settings.DATABASES[dbname]['PORT']
            if port:
                _connection_settings['port'] = int(port)
            _db_name = settings.DATABASES[dbname]['NAME']
            break
except ImportError:
    pass


class ConnectionError(Exception):
    pass


def _get_connection():
    global _connection
    # Connect to the database if not already connected
    if _connection is None:
        try:
            _connection = Connection(**_connection_settings)
        except:
            raise ConnectionError('Cannot connect to the database')
    return _connection

def _get_db():
    global _db, _connection
    # Connect if not already connected
    if _connection is None:
        _connection = _get_connection()

    if _db is None:
        # _db_name will be None if the user hasn't called connect()
        if _db_name is None:
            raise ConnectionError('Not connected to the database')

        # Get DB from current connection and authenticate if necessary
        _db = _connection[_db_name]
        if _db_username and _db_password:
            _db.authenticate(_db_username, _db_password)
    if TransformDjango:
        _db.add_son_manipulator(TransformDjango())

    return _db

def connect(db, username=None, password=None, **kwargs):
    """Connect to the database specified by the 'db' argument. Connection 
    settings may be provided here as well if the database is not running on
    the default port on localhost. If authentication is needed, provide
    username and password arguments as well.
    """
    global _connection_settings, _db_name, _db_username, _db_password
    _connection_settings.update(kwargs)
    _db_name = db
    _db_username = username
    _db_password = password
    return _get_db()