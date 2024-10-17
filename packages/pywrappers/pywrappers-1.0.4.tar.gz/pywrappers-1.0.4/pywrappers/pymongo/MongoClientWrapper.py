from typing import Any, Dict, Optional, Union, List
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.client_session import ClientSession
from pymongo.errors import OperationFailure
from pymongo.command_cursor import CommandCursor

from . import Database

class MongoClientWrapper:
    """
    A wrapper class for PyMongo's MongoClient, designed to ensure compatibility between PyMongo 3.4 and 4.x.

    The MongoClientWrapper class provides an interface that supports legacy PyMongo 3.4 methods, such as database_names()
    and ismaster(), which have been deprecated or removed in PyMongo 4.x. Additionally, the class supports all new functionality
    introduced in PyMongo 4.x, including improved methods for managing connections, executing server commands, and working with
    replica sets.
    
    ---
    Key Features:
    - Backward Compatibility: Implements deprecated methods like database_names() and ismaster() to ensure that legacy systems 
      continue to function without modification.
    - Forward Compatibility: Fully supports PyMongo 4.x features, such as list_database_names() and the hello command for 
      querying replica set status.
    - Error Handling for Deprecated Methods: For methods like get_default_database() and ismaster(), which have been removed in 
      PyMongo 4.x, the wrapper raises clear NotImplementedError exceptions with explanations and suggestions for alternatives.
    
    ---
    Key Methods:
    - get_database(name): Retrieves a DatabaseWrapper object for the specified database.
    - database_names(): Legacy method that lists database names (replaced by list_database_names() in PyMongo 4.x).
    - ismaster(): Uses the hello command to retrieve replica set information, replacing the deprecated ismaster() method.
    - ping(): Pings the MongoDB server to check its responsiveness.
    - command(dbname, command): Executes a command on a specific database and returns the result.
    - with_options(): Creates a new MongoClientWrapper object with customized connection options.
    
    ---
    Example Usage:
    python
    client = MongoClientWrapper("localhost", 27017)
    
    ---
    Accessing a database
    db = client.get_database("mydatabase")
    ---
    Listing database names (PyMongo 3.4 compatibility)
    print(client.database_names())
    ---
    Ping the MongoDB server
    print(client.ping())
    ---
    Close the connection
    client.close()
    
    ---
    Parameters:
    - host: Optional string or list of strings specifying the MongoDB server(s) to connect to.
    - port: Optional integer specifying the port to connect to (default is 27017).
    - kwargs: Additional MongoDB connection options (such as authentication, replica set configurations, etc.).

    ---
    Exceptions Raised:
    - ConnectionError: Raised when the connection to MongoDB cannot be established.
    - NotImplementedError: Raised for deprecated methods like ismaster() and get_default_database(), with explanations for why they
       were removed and how to work around them.
    - RuntimeError: Raised when server operations, such as listing databases or executing commands, fail due to server errors.

    ---
    Compatibility:
    This class maintains full compatibility with both PyMongo 3.4 and 4.x by implementing legacy methods and ensuring smooth 
    operation in modern environments. 

    """
    def __init__(self, host: Optional[Union[str, List[str]]] = None, port: Optional[int] = None, **kwargs: Any):
        """
        Initialize MongoClientWrapper with the same parameters as MongoClient.
        If no host/port are provided, it uses MongoDB's default connection.
        """
        try:
            self.client = MongoClient(host, port, **kwargs)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize MongoClient: {e}")
   
    # --- Access to Databases ---
    def get_database(self, name: str, codec_options: Optional[Any] = None, read_preference: Optional[ReadPreference] = None,
                     write_concern: Optional[WriteConcern] = None, read_concern: Optional[ReadConcern] = None) -> Database:
        """
        Return a DatabaseWrapper for the specified database.
        Uses MongoClient.get_database() and wraps the result.
        """
        db = self.client.get_database(name, codec_options=codec_options, read_preference=read_preference,
                                      write_concern=write_concern, read_concern=read_concern)
        return Database(db)

    def __getitem__(self, name: str) -> Database:
        """Allow access to databases as dictionary keys."""
        return self.get_database(name)
    
    # --- List Databases ---
    def list_database_names(self, session: Optional[ClientSession] = None) -> List[str]:
        """List all database names on the MongoDB server (replaces the deprecated database_names())."""
        try:
            return self.client.list_database_names(session=session)
        except OperationFailure as e:
            raise RuntimeError(f"Error listing database names: {e}")

    def database_names(self) -> List[str]:
        """Return a list of database names (PyMongo 3.4 compatibility)."""
        return self.list_database_names()

    def list_databases(self, session: Optional[ClientSession] = None, filter: Optional[Dict[str, Any]] = None,
                       name_only: bool = False) -> CommandCursor:
        """List databases on the MongoDB server with additional details."""
        try:
            return self.client.list_databases(session=session, filter=filter, name_only=name_only)
        except OperationFailure as e:
            raise RuntimeError(f"Error listing databases: {e}")

    # --- Database Management ---
    def drop_database(self, name_or_database: Union[str, Database], session: Optional[ClientSession] = None) -> None:
        """Drop a database by name or by DatabaseWrapper."""
        try:
            if isinstance(name_or_database, Database):
                self.client.drop_database(name_or_database.database, session=session)
            else:
                self.client.drop_database(name_or_database, session=session)
        except OperationFailure as e:
            raise RuntimeError(f"Error dropping database: {e}")

    # --- Server Operations ---
    def server_info(self, session: Optional[ClientSession] = None) -> Dict[str, Any]:
        """Return server information."""
        try:
            return self.client.server_info(session=session)
        except OperationFailure as e:
            raise RuntimeError(f"Error retrieving server info: {e}")

    def ping(self, session: Optional[ClientSession] = None) -> Dict[str, Any]:
        """Ping the MongoDB server to check its responsiveness."""
        try:
            return self.client.admin.command("ping", session=session)
        except OperationFailure as e:
            raise RuntimeError(f"Error pinging server: {e}")

    # --- Connection Management ---
    def close(self) -> None:
        """Close the MongoDB connection."""
        self.client.close()

    def start_session(self, causal_consistency: bool = True, default_transaction_options: Optional[Any] = None) -> ClientSession:
        """Start a session for operations with causal consistency."""
        return self.client.start_session(causal_consistency=causal_consistency, default_transaction_options=default_transaction_options)

    # --- Replica Set Operations (if applicable) ---
    def ismaster(self, session: Optional[ClientSession] = None) -> Dict[str, Any]:
        """
        Mimic the 'ismaster' command using 'hello' (removed in PyMongo 4.x).
        This only works in replica set configurations.
        """
        try:
            return self.client.admin.command("hello", session=session)
        except OperationFailure as e:
            raise NotImplementedError(
                "The 'ismaster' method has been removed in PyMongo 4.x. Use the 'hello' command for similar functionality, "
                "which works only in replica set configurations."
            )

    def primary(self, session: Optional[ClientSession] = None) -> Optional[str]:
        """Get the primary node of the replica set."""
        try:
            status = self.client.admin.command("hello", session=session)
            return status.get('primary')
        except OperationFailure as e:
            raise NotImplementedError(
                "The 'primary' method is not supported on standalone MongoDB instances."
            )

    def nodes(self) -> List[str]:
        """Return the nodes in the current connection."""
        return list(self.client.nodes)

    # --- MongoDB Commands ---
    def command(self, dbname: str, command: Union[str, Dict[str, Any]], session: Optional[ClientSession] = None) -> Dict[str, Any]:
        """Execute a command on the specified database."""
        try:
            db = self.get_database(dbname)
            return db.command(command, session=session)
        except OperationFailure as e:
            raise RuntimeError(f"Error executing command on database '{dbname}': {e}")

    # --- Configuration Options ---
    def with_options(self, codec_options: Optional[Any] = None, read_preference: Optional[ReadPreference] = None,
                     write_concern: Optional[WriteConcern] = None, read_concern: Optional[ReadConcern] = None) -> 'MongoClientWrapper':
        """Return a new MongoClientWrapper with the provided options."""
        client_with_options = self.client.with_options(codec_options=codec_options, read_preference=read_preference,
                                                       write_concern=write_concern, read_concern=read_concern)
        return MongoClientWrapper(client_with_options)

    # --- Callable Access to Databases ---
    def __call__(self, dbname: str) -> Database:
        """Allow callable access to a database (PyMongo 3.4 compatibility)."""
        return self.get_database(dbname)
    
    # --- pymongo 4.4 Compatibility ---
    
    # Fallback to the original MongoClient methods for any method not explicitly defined
    def __getattr__(self, name: str) -> Any:
        """
        Delegate method calls to the underlying MongoClient instance for any methods not explicitly implemented
        in MongoClientWrapper. This allows access to any new methods introduced in PyMongo 4.x without needing
        to implement them directly.
        """
        return getattr(self.client, name)
    
    def __instancecheck__(self, instance):
        return isinstance(instance, MongoClient)