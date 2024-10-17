import importlib
import pymongo

from typing import Any

# Check if pymongo version is 4.0 or higher
version = pymongo.version_tuple
if version < (4, 0):
    raise ImportError(
        "The installed pymongo version is below 4.0. This package requires pymongo>=4.0. "
        "Please upgrade your pymongo package."
    )

# Cache for imported modules
_import_cache = {}

# Lazy load function to load pymongo components when necessary
def lazy_import(module: str, name: str) -> Any:
    """Dynamically import a module to support lazy imports.
    
    Args:
        module (str): The module to import.
        name (str): The specific attribute or class to load from the module.

    Returns:
        Any: The module's attribute or class.
    """
    if module not in _import_cache:
        _import_cache[module] = importlib.import_module(module)
    return getattr(_import_cache[module], name)


# Lazy imports for PyMongo 4.4 constants, errors, and operations
ReadPreference = lazy_import('pymongo.read_preferences', 'ReadPreference')
WriteConcern = lazy_import('pymongo.write_concern', 'WriteConcern')
ReadConcern = lazy_import('pymongo.read_concern', 'ReadConcern')
ASCENDING = lazy_import('pymongo', 'ASCENDING')
DESCENDING = lazy_import('pymongo', 'DESCENDING')
GEOSPHERE = lazy_import('pymongo', 'GEOSPHERE')
TEXT = lazy_import('pymongo', 'TEXT')
HASHED = lazy_import('pymongo', 'HASHED')
ReturnDocument = lazy_import('pymongo.collection', 'ReturnDocument')
CommandCursor = lazy_import('pymongo.command_cursor', 'CommandCursor')
ClientSession = lazy_import('pymongo.client_session', 'ClientSession')

# Authentication mechanisms
MECHANISMS = lazy_import('pymongo.auth', 'MECHANISMS')

# PyMongo MongoClient, Database and Collection classes
PyMongoClient = lazy_import('pymongo', 'MongoClient')
PyDatabase = lazy_import('pymongo.database', 'Database')
PyCollection = lazy_import('pymongo.collection', 'Collection')

# Errors
BulkWriteError = lazy_import('pymongo.errors', 'BulkWriteError')
InvalidOperation = lazy_import('pymongo.errors', 'InvalidOperation')
OperationFailure = lazy_import('pymongo.errors', 'OperationFailure')
ConfigurationError = lazy_import('pymongo.errors', 'ConfigurationError')
ConnectionFailure = lazy_import('pymongo.errors', 'ConnectionFailure')
CursorNotFound = lazy_import('pymongo.errors', 'CursorNotFound')
ExecutionTimeout = lazy_import('pymongo.errors', 'ExecutionTimeout')
WriteError = lazy_import('pymongo.errors', 'WriteError')
WriteConcernError = lazy_import('pymongo.errors', 'WriteConcernError')
PyMongoError = lazy_import('pymongo.errors', 'PyMongoError')
DuplicateKeyError = lazy_import('pymongo.errors', 'DuplicateKeyError')
CollectionInvalid = lazy_import('pymongo.errors', 'CollectionInvalid')
NetworkTimeout = lazy_import('pymongo.errors', 'NetworkTimeout')
ServerSelectionTimeoutError = lazy_import('pymongo.errors', 'ServerSelectionTimeoutError')
DocumentTooLarge = lazy_import('pymongo.errors', 'DocumentTooLarge')
InvalidName = lazy_import('pymongo.errors', 'InvalidName')

# Operations
InsertOne = lazy_import('pymongo.operations', 'InsertOne')
DeleteOne = lazy_import('pymongo.operations', 'DeleteOne')
DeleteMany = lazy_import('pymongo.operations', 'DeleteMany')
UpdateOne = lazy_import('pymongo.operations', 'UpdateOne')
UpdateMany = lazy_import('pymongo.operations', 'UpdateMany')
ReplaceOne = lazy_import('pymongo.operations', 'ReplaceOne')
IndexModel = lazy_import('pymongo.operations', 'IndexModel')
SearchIndexModel = lazy_import('pymongo.operations', 'SearchIndexModel')

# Wrappers from the custom implementation
from .CollectionWrapper import CollectionWrapper as Collection
from .DatabaseWrapper import DatabaseWrapper as Database
from .MongoClientWrapper import MongoClientWrapper as MongoClient

# Expose the necessary classes, constants, and errors to users
__all__ = [
    # Wrappers
    'MongoClient', 'Database', 'Collection',
    
    # PyMongo 4.4 Constants and Classes
    'PyMongoClient', 'ReadPreference', 'WriteConcern', 'ReadConcern',
    'ASCENDING', 'DESCENDING', 'GEOSPHERE', 'TEXT', 'HASHED', 'ReturnDocument',
    
    # PyMongo 4.4 Errors
    'BulkWriteError', 'InvalidOperation', 'OperationFailure', 'ConfigurationError',
    'ConnectionFailure', 'CursorNotFound', 'ExecutionTimeout', 'WriteError',
    'WriteConcernError', 'PyMongoError', 'DuplicateKeyError', 'CollectionInvalid',
    'NetworkTimeout', 'ServerSelectionTimeoutError', 'DocumentTooLarge', 'InvalidName',
    
    # PyMongo 4.4 Operations
    'InsertOne', 'DeleteOne', 'DeleteMany', 'UpdateOne', 'UpdateMany', 'ReplaceOne',
    'IndexModel', 'SearchIndexModel'
]