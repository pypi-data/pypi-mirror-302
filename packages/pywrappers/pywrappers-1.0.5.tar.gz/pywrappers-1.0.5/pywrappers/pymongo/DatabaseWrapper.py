from typing import Any, Dict, Optional, Union, List
from pymongo.database import Database
from pymongo.command_cursor import CommandCursor
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from pymongo.client_session import ClientSession
from pymongo.read_concern import ReadConcern
from bson.dbref import DBRef

from . import Collection


class DatabaseWrapper:
    """
    A wrapper class for PyMongo's Database object, designed to maintain compatibility between PyMongo 3.4 and 4.x.

    The DatabaseWrapper class provides an interface that supports legacy PyMongo 3.4 methods, such as collection_names(), authenticate(), and eval(), which have been deprecated or removed in PyMongo 4.x. The class ensures backward compatibility while also fully supporting the functionality introduced in PyMongo 4.x.
    ---
    Key Features:
    - Backward Compatibility: Implements deprecated methods like collection_names(), add_user(), remove_user(), authenticate(), and eval(), ensuring that legacy systems can continue to function without modification.
    - Forward Compatibility: All current PyMongo 4.x methods are fully supported, including methods for managing collections, executing commands, and handling database-level options such as read_concern, write_concern, and read_preference.
    - Error Handling for Deprecated Methods: For methods like authenticate() and eval(), which have been completely removed in PyMongo 4.x, the wrapper raises descriptive NotImplementedError exceptions, explaining the change and suggesting alternative approaches (e.g., using URI-based authentication or the Aggregation Framework).
    ---
    Main Methods:
    - get_collection(): Retrieves a collection from the database and wraps it in a CollectionWrapper.
    - collection_names(): Returns a list of collection names, maintaining compatibility with PyMongo 3.4.
    - create_collection(): Creates a new collection in the database and returns it wrapped in CollectionWrapper.
    - drop_collection(): Drops a collection from the database.
    - command(): Executes a command on the database.
    - authenticate(): Removed in PyMongo 4.x. Raises NotImplementedError with guidance on how to handle authentication via connection strings.
    - eval(): Removed in MongoDB 4.x. Raises NotImplementedError and suggests using the Aggregation Framework or MapReduce for similar functionality.
    - add_user(): Adds a user to the database (PyMongo 3.4 compatibility).
    - remove_user(): Removes a user from the database (PyMongo 3.4 compatibility).
    - dereference(): Dereferences a DBRef object.
    ---
    Example Usage:
    
    db = client.get_database("my_database")
    wrapped_db = DatabaseWrapper(db)

    Retrieve a collection
    collection = wrapped_db.get_collection("my_collection")

    Drop a collection
    wrapped_db.drop_collection("my_collection")

    Run a command on the database
    result = wrapped_db.command("ping")
    ---
    Parameters:
    - database: A Database object from PyMongo that will be wrapped by this class.
    ---
    Exceptions Raised:
    - NotImplementedError: Raised for deprecated methods such as authenticate() and eval(), with explanations for why they were removed and how to work around them.
    """
    def __init__(self, database: Database):
        """Initialize the DatabaseWrapper with a valid Database object."""
        if not isinstance(database, Database):
            raise TypeError("Expected 'database' to be an instance of pymongo.database.Database.")
        self.database = database

    # --- Collection Management Methods ---
    def get_collection(self, name: str, codec_options: Optional[Any] = None, read_preference: Optional[ReadPreference] = None, 
                       write_concern: Optional[WriteConcern] = None, read_concern: Optional[ReadConcern] = None) -> Collection:
        """Get a collection from the database and wrap it with CollectionWrapper."""
        collection = self.database.get_collection(name, codec_options=codec_options, 
                                                  read_preference=read_preference, 
                                                  write_concern=write_concern, 
                                                  read_concern=read_concern)
        return Collection(collection=collection)

    def __getitem__(self, name: str) -> Collection:
        """Allow access to collections as dictionary keys."""
        return self.get_collection(name)
    
    # Implemented for compatibility with the deprecated database.collection_names() from PyMongo 3.4
    def collection_names(self, include_system_collections: bool = True, session: Optional[ClientSession] = None) -> List[str]:
        """
        Return a list of collection names in the database (compatible with PyMongo 3.4).
        PyMongo 4.x replaced collection_names() with list_collection_names().
        """
        if include_system_collections:
            return self.database.list_collection_names(session=session)
        return [name for name in self.database.list_collection_names(session=session) if not name.startswith("system.")]

    def create_collection(self, name: str, codec_options: Optional[Any] = None, 
                          read_preference: Optional[ReadPreference] = None, write_concern: Optional[WriteConcern] = None,
                          read_concern: Optional[ReadConcern] = None, session: Optional[ClientSession] = None, **kwargs: Any) -> Collection:
        """Create a new collection in the database and return it wrapped with CollectionWrapper."""
        collection = self.database.create_collection(name, codec_options=codec_options, 
                                                     read_preference=read_preference, 
                                                     write_concern=write_concern, 
                                                     read_concern=read_concern, 
                                                     session=session, **kwargs)
        return Collection(collection)

    def drop_collection(self, name_or_collection: Union[str, Collection], session: Optional[ClientSession] = None) -> None:
        """Drop a collection from the database."""
        if isinstance(name_or_collection, Collection):
            self.database.drop_collection(name_or_collection.collection, session=session)
        else:
            self.database.drop_collection(name_or_collection, session=session)

    def list_collections(self, session: Optional[ClientSession] = None, filter: Optional[Dict[str, Any]] = None) -> CommandCursor:
        """List all collections in the database."""
        return self.database.list_collections(session=session, filter=filter)

    # --- Database Command Methods ---
    def command(self, command: Union[Dict[str, Any], str], value: Any = 1, check: bool = True, allowable_errors: Optional[List[str]] = None, 
                read_preference: Optional[ReadPreference] = None, session: Optional[ClientSession] = None, **kwargs: Any) -> Dict[str, Any]:
        """Execute a command on the database."""
        return self.database.command(command, value=value, check=check, allowable_errors=allowable_errors, 
                                     read_preference=read_preference, session=session, **kwargs)

    def drop(self, session: Optional[ClientSession] = None) -> None:
        """Drop the entire database."""
        self.database.drop(session=session)

    # --- Compatibility Methods (for deprecated functionality) ---
    # Authenticate: Method removed in PyMongo 4.x
    def authenticate(self, name: str, password: Optional[str] = None, source: Optional[str] = None, mechanism: Optional[str] = None) -> None:
        """Authenticate a user (removed in PyMongo 4.x)."""
        raise NotImplementedError(
            """The authenticate() method was removed in PyMongo 4.x. Authentication must now be performed directly in the connection string.
            Use the authSource or authMechanism parameters in the connection URI to handle authentication."""
        )

    # Eval: Method removed in MongoDB 4.x
    def eval(self, code: str, args: Optional[Any] = None, nolock: bool = False) -> None:
        """Evaluate JavaScript on the server (removed in MongoDB 4.x)."""
        raise NotImplementedError(
            """The eval() method was removed in MongoDB 4.x for security and performance reasons.
            Use the Aggregation Framework or MapReduce to achieve similar functionality."""
        )

    # User Management Methods (PyMongo 3.4 Compatibility)
    def add_user(self, name: str, password: Optional[str] = None, roles: Optional[List[str]] = None, 
                 read_only: Optional[bool] = None, **kwargs: Any) -> None:
        """Add a user to the database (compatibility with PyMongo 3.4)."""
        if roles is None:
            roles = ['readWrite' if not read_only else 'read']
        self.database.command("createUser", name, pwd=password, roles=roles, **kwargs)

    def remove_user(self, name: str) -> None:
        """Remove a user from the database (compatibility with PyMongo 3.4)."""
        self.database.command("dropUser", name)

    # --- DBRef Management ---
    def dereference(self, dbref: DBRef, session: Optional[ClientSession] = None) -> Optional[Dict[str, Any]]:
        """Dereference a DBRef object."""
        return self.database.dereference(dbref, session=session)

    # --- Database Option Handling ---
    def with_options(self, codec_options: Optional[Any] = None, read_preference: Optional[ReadPreference] = None, 
                     write_concern: Optional[WriteConcern] = None, read_concern: Optional[ReadConcern] = None) -> 'DatabaseWrapper':
        """Return a new DatabaseWrapper with the given options."""
        db_with_options = self.database.with_options(codec_options=codec_options, read_preference=read_preference, 
                                                     write_concern=write_concern, read_concern=read_concern)
        return DatabaseWrapper(db_with_options)

    # --- Database Properties ---
    @property
    def write_concern(self) -> WriteConcern:
        """Return the write concern of the database."""
        return self.database.write_concern

    @property
    def read_concern(self) -> ReadConcern:
        """Return the read concern of the database."""
        return self.database.read_concern

    @property
    def read_preference(self) -> ReadPreference:
        """Return the read preference of the database."""
        return self.database.read_preference

    @property
    def name(self) -> str:
        """Return the name of the database."""
        return self.database.name
    
    # --- Callable Access to Collections ---

    def __call__(self, name: str) -> Collection:
        """Allow access to collections as attributes of the database."""
        return self.get_collection(name)
    
    # --- pymongo 4.4 Compatibility ---
    
    # Fallback to the original MongoClient methods for any method not explicitly defined
    def __getattr__(self, name: str) -> Any:
        """
        Delegate method calls to the underlying MongoClient instance for any methods not explicitly implemented
        in MongoClientWrapper. This allows access to any new methods introduced in PyMongo 4.x without needing
        to implement them directly.
        """
        return getattr(self.database, name)
    
    def __instancecheck__(self, instance):
        return isinstance(instance, Database)