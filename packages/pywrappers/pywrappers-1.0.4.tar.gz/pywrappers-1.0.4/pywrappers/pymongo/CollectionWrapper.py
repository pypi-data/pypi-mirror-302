from typing import Any, List, Dict, Optional, Union, Tuple
from pymongo.results import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult, BulkWriteResult
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo import InsertOne, UpdateOne, UpdateMany, DeleteOne, DeleteMany
from pymongo.errors import BulkWriteError

class CollectionWrapper:
    """
    A wrapper class for PyMongo's Collection object, designed to ensure compatibility with both PyMongo 3.4 and 4.4.

    The `CollectionWrapper` provides a transparent interface for interacting with a MongoDB collection while maintaining
    the syntax and functionality of deprecated methods from PyMongo 3.4, such as `insert()`, `update()`, `remove()`, and
    `map_reduce()`. These methods are mapped to their PyMongo 4.x equivalents (`insert_one()`, `update_one()`, 
    `delete_one()`, etc.) to ensure seamless operation of legacy codebases.

    Additionally, the class retains all existing PyMongo 4.x functionality, supporting both CRUD operations, aggregation 
    pipelines, bulk operations, index management, and collection-level administrative tasks.
    ---
    Key Features:
    - **Backward Compatibility**: Implements deprecated methods from PyMongo 3.4, ensuring existing code can run on PyMongo 4.x without modifications.
    - **Forward Compatibility**: Fully supports all new methods and enhancements introduced in PyMongo 4.x.
    - **Error Handling**: Includes robust error handling and descriptive exception messages to guide users through failures like bulk write errors.
    - **Type Safety**: Utilizes Python's `typing` module for explicit type declarations, improving code clarity and reducing runtime errors.

    Methods Implemented for Compatibility:
    - `insert()`: Now directs to `insert_one()` or `insert_many()`.
    - `update()`: Now directs to `update_one()` or `update_many()`.
    - `remove()`: Now directs to `delete_one()` or `delete_many()`.
    - `map_reduce()`: Not implemented in PyMongo 4.x, raises a `NotImplementedError` suggesting alternative use of aggregation.
    ---
    Example Usage:

    collection = db.get_collection("users")
    wrapped_collection = CollectionWrapper(collection)

    # Insert a single document (compatible with PyMongo 3.4's insert())
    wrapped_collection.insert({"name": "Alice", "age": 30})

    # Find and update a document
    wrapped_collection.update({"name": "Alice"}, {"$set": {"age": 31}})
    ---
    Parameters:
    - collection: The PyMongo Collection object that will be wrapped.
    """
    def __init__(self, collection: Collection):
        """Initialize the CollectionWrapper with a valid Collection object."""
        if not isinstance(collection, Collection):
            raise TypeError("Expected 'collection' to be an instance of pymongo.collection.Collection.")
        self.collection = collection

    # --- Insert Methods ---
    def insert_one(self, document: Dict[str, Any]) -> InsertOneResult:
        """Insert a single document into the collection."""
        return self.collection.insert_one(document)

    def insert_many(self, documents: List[Dict[str, Any]], ordered: bool = True) -> InsertManyResult:
        """Insert multiple documents into the collection."""
        return self.collection.insert_many(documents, ordered=ordered)

    # Implemented for compatibility with the deprecated insert() in PyMongo 3.4
    def insert(self, doc_or_docs: Union[Dict[str, Any], List[Dict[str, Any]]], manipulate: bool = True, check_keys: bool = True, continue_on_error: bool = False) -> Union[InsertOneResult, InsertManyResult]:
        """
        Handles the deprecated insert() method by directing calls to insert_one() or insert_many().
        This ensures compatibility with PyMongo 3.4, where insert() was a common operation.
        """
        if isinstance(doc_or_docs, list):
            return self.insert_many(doc_or_docs, ordered=not continue_on_error)
        return self.insert_one(doc_or_docs)

    # --- Update Methods ---
    def update_one(self, filter: Dict[str, Any], update: Dict[str, Any], upsert: bool = False) -> UpdateResult:
        """Update a single document matching the filter."""
        return self.collection.update_one(filter, update, upsert=upsert)

    def update_many(self, filter: Dict[str, Any], update: Dict[str, Any], upsert: bool = False) -> UpdateResult:
        """Update multiple documents matching the filter."""
        return self.collection.update_many(filter, update, upsert=upsert)

    # Implemented for compatibility with the deprecated update() in PyMongo 3.4
    def update(self, spec: Dict[str, Any], document: Dict[str, Any], upsert: bool = False, multi: bool = False) -> UpdateResult:
        """
        Handles the deprecated update() method by directing calls to update_one() or update_many().
        This ensures compatibility with PyMongo 3.4, where update() was commonly used.
        """
        if multi:
            return self.update_many(spec, document, upsert=upsert)
        return self.update_one(spec, document, upsert=upsert)

    # --- Delete Methods ---
    def delete_one(self, filter: Dict[str, Any]) -> DeleteResult:
        """Delete a single document matching the filter."""
        return self.collection.delete_one(filter)

    def delete_many(self, filter: Dict[str, Any]) -> DeleteResult:
        """Delete multiple documents matching the filter."""
        return self.collection.delete_many(filter)

    # Implemented for compatibility with the deprecated remove() in PyMongo 3.4
    def remove(self, spec_or_id: Union[Dict[str, Any], Any], multi: bool = False) -> DeleteResult:
        """
        Handles the deprecated remove() method by directing calls to delete_one() or delete_many().
        This ensures compatibility with PyMongo 3.4, where remove() was a standard operation.
        """
        if multi:
            return self.delete_many(spec_or_id)
        return self.delete_one(spec_or_id)

    # --- Find Methods ---
    def find(self, filter: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any) -> Cursor:
        """Find documents in the collection based on a filter."""
        return self.collection.find(filter, *args, **kwargs)

    def find_one(self, filter: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Find a single document in the collection."""
        return self.collection.find_one(filter, *args, **kwargs)

    def find_one_and_update(self, filter: Dict[str, Any], update: Dict[str, Any], *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Find and update a single document in the collection."""
        return self.collection.find_one_and_update(filter, update, *args, **kwargs)

    def find_one_and_delete(self, filter: Dict[str, Any], *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Find and delete a single document from the collection."""
        return self.collection.find_one_and_delete(filter, *args, **kwargs)

    def find_one_and_replace(self, filter: Dict[str, Any], replacement: Dict[str, Any], *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Find and replace a single document in the collection."""
        return self.collection.find_one_and_replace(filter, replacement, *args, **kwargs)

    # --- Bulk Operations ---
    def bulk_write(self, requests: List[Union[InsertOne, UpdateOne, UpdateMany, DeleteOne, DeleteMany]], ordered: bool = True) -> BulkWriteResult:
        """
        Perform multiple write operations in bulk (insert, update, delete).
        Provides detailed error message on BulkWriteError.
        """
        try:
            return self.collection.bulk_write(requests, ordered=ordered)
        except BulkWriteError as bwe:
            raise BulkWriteError(f"Bulk write operation failed: {bwe.details}")

    # --- Count Methods ---
    def count_documents(self, filter: Dict[str, Any]) -> int:
        """Count documents matching the filter."""
        return self.collection.count_documents(filter)

    def estimated_document_count(self, **kwargs: Any) -> int:
        """Estimate the number of documents in the collection."""
        return self.collection.estimated_document_count(**kwargs)

    # --- Index Operations ---
    def create_index(self, keys: Union[List[Tuple[str, int]], Dict[str, int]], **kwargs: Any) -> str:
        """Create an index on the collection."""
        return self.collection.create_index(keys, **kwargs)

    def create_indexes(self, indexes: List[Any]) -> List[str]:
        """Create multiple indexes on the collection."""
        return self.collection.create_indexes(indexes)

    def list_indexes(self) -> Cursor:
        """List all indexes on the collection."""
        return self.collection.list_indexes()

    def drop_index(self, index_name: str, **kwargs: Any) -> None:
        """Drop a specific index from the collection."""
        self.collection.drop_index(index_name, **kwargs)

    def drop_indexes(self) -> None:
        """Drop all indexes on the collection."""
        self.collection.drop_indexes()

    # --- Aggregation Methods ---
    def aggregate(self, pipeline: List[Dict[str, Any]], **kwargs: Any) -> Cursor:
        """Aggregate documents using a pipeline."""
        return self.collection.aggregate(pipeline, **kwargs)

    def distinct(self, key: str, filter: Optional[Dict[str, Any]] = None, **kwargs: Any) -> List[Any]:
        """Return distinct values for a specific key."""
        return self.collection.distinct(key, filter, **kwargs)

    # --- Change Streams (requires replica set) ---
    def watch(self, pipeline: Optional[List[Dict[str, Any]]] = None, **kwargs: Any) -> Any:
        """Watch for changes in the collection (replica set required)."""
        return self.collection.watch(pipeline, **kwargs)

    # --- Collection Management ---
    def rename(self, new_name: str, **kwargs: Any) -> None:
        """Rename the collection."""
        self.collection.rename(new_name, **kwargs)

    def drop(self) -> None:
        """Drop the collection."""
        self.collection.drop()

    # Implemented for compatibility with the deprecated map_reduce() in PyMongo 3.4
    def map_reduce(self, map: str, reduce: str, out: Union[str, Dict[str, Any]], full_response: bool = False, **kwargs: Any) -> Any:
        """
        Raise NotImplementedError for map_reduce(), removed in PyMongo 4.x.
        PyMongo 3.4 supported map_reduce, but this operation is no longer available in 4.x.
        """
        raise NotImplementedError("map_reduce was removed in PyMongo 4.x. Use the aggregation framework instead.")
    
    # --- pymongo 4.4 Compatibility ---
    
    # Fallback to the original MongoClient methods for any method not explicitly defined
    def __getattr__(self, name: str) -> Any:
        """
        Delegate method calls to the underlying MongoClient instance for any methods not explicitly implemented
        in MongoClientWrapper. This allows access to any new methods introduced in PyMongo 4.x without needing
        to implement them directly.
        """
        return getattr(self.collection, name)
    
    def __instancecheck__(self, instance):
        return isinstance(instance, Collection)