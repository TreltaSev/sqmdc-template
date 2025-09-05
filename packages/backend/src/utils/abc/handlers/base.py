# === Core ===
import random

# === Typing ===
from pydantic import BaseModel
from pymongo.collection import Collection
from typing import Any, ClassVar, Optional, Self
from pymongo.results import UpdateResult, InsertOneResult


class WrapperModel(BaseModel):
    """
    Wrapper for :class:`pydantic.BaseModel` that has some default functionality for all children
    classes.
    """

    __collection__: ClassVar[Collection]

    class Config:
        extra = "allow"

    # === Creation & Serialization ===
    def safe_dump(self, *args, **kwargs) -> dict[str, Any]:
        """
        Dumps the model to a dictionary while stripping reserved or internal-use fields

        Wraps :meth:`pydantic.BaseModel.model_dump` and removes keys that may cause issues
        when persisting the model to the database (e.g., `_id` duplication errors).

        Removes
        -------
        - `_id`
            Avoids inserting explicit `_id: None` values that could trigger duplicate key errors

        :param Any args: Positional arguments passed to `model_dump`
        :param Any kwargs: Keyword arguments passed to `model_dump`
        :returns dict[str, Any]: Serialized dictionary representation of the model
        """

        # Default Behavior
        document = self.model_dump(*args, **kwargs)

        # Remove Crucial Keys
        document.pop("_id", None)

        return document

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new model instance from the provided dictionary data

        Instantiates the model using keyword arguments unpacked from the input dictionary,
        without performing any database interaction.

        :param dict data: Dictionary of field values for the new model instance
        :returns Self: Instantiated model object
        """

        instance = cls(**kwargs)

        # Handle After Update Logic
        after_create = getattr(instance, "after_create", None)
        if callable(after_create):
            result = after_create(instance)
            if isinstance(result, cls):
                return result
            return instance
        return instance

    def insert(self) -> Self:
        """
        Inserts the current model instance into the database and returns the instance

        This is a convenience method that wraps `insert_low` and returns `self` to allow
        for method chaining. It does not return the raw MongoDB result, only the object itself.

        Usage
        -----
        This enables chaining like:
            user = User.create(...).insert()

        :returns Self: The model instance that was inserted
        """

        self.insert_low()
        return self

    def insert_low(self) -> InsertOneResult:
        """
        Inserts the current object into the database

        :returns pymongo.results.InsertOneResult: Result of the insert operation
        """
        document = self.safe_dump()
        return self.__collection__.insert_one(document)

    # === Retrieval & Existence ===

    @classmethod
    def get(cls, **filters) -> Self:
        """
        Retrieves a document from the collection based on the provided filters

        Executes a MongoDB `find_one` query using the given filter arguments and constructs
        a model instance from the result. Must be called from the class rather than an instance.

        :param kwargs filters: MongoDB filter to locate the document
        :raises LookupError: If no matching document is found
        :returns Self: A model instance containing the document's data
        """

        search = cls.__collection__.find_one(filters)
        if not search:
            raise LookupError(f"Failed to find document, filters: {filters}")
        return cls(**search)
    
    @classmethod
    def random(cls) -> Optional[Self]:
        """
        Returns a random instance of itself, if there are no instances
        within the database, then return None
        
        :returns Optional[Self]: Random instance of self or None
        """
        
        # Get entire collection as cursor
        docs_cursor = cls.__collection__.find({})
        
        # Go through cursor and save to array
        docs = [docs_item for docs_item in docs_cursor]
        
        return random.choice(docs) if len(docs) > 0 else None

    @classmethod
    def exists(cls, **filters):
        """
        Checks whether a document exists in the collection based on the provided filters

        Executes a MongoDB `find_one` query and returns a boolean indicating whether
        a document matching the filters was found.

        :param kwargs filters: MongoDB filter to locate the document
        :returns bool: True if a document exists, False otherwise
        """

        if cls.__collection__.find_one(filters):
            return True
        return False

    # === Modification ===

    def update(self, filter: dict[str, Any] = None, operation: str = "", update: dict[str, Any] = {}) -> UpdateResult:
        """
        Updates a document in the given collection using the specified operation and filter

        :param dict[str, Any] filter: Filter object to locate the target document
        :param str operation: MongoDB update operation (e.g., "$set", "$unset", "$inc")
        :param dict[str, Any] update: Fields and values to apply with the specified operation
        :returns pymongo.results.UpdateResult: Result object containing matched and modified counts
        """

        if filter is None:
            filtered_id = getattr(self, "id", None) or getattr(self, "_id", None) or None
            key: bool = "id"
            value = None

            if hasattr(self, "id"):
                value = getattr(self, "id")
            elif hasattr(self, "_id"):
                value = getattr(self, "_id")
                key = "_id"

            if not value:
                raise ValueError("No filter was specified and no conclusions could be drawn")

            filter = {key: value}

        return self.__collection__.update_one(filter, {operation: update})

    def set(self, update: dict[str, Any], **filters) -> None:
        """
        Applies a set operation to the user document in the database

        :param dict[str, Any] update: Fields and values to update in the document
        :param kwargs filters: MongoDB filter to locate the target document
        """
        if not filters and hasattr(self, "id"):
            filters = {"id": self.id}

        self.update(filters, "$set", update)
        self.refresh()

    def refresh(self, **filters) -> None:
        """
        Refreshes the current model instance with the latest data from the database

        Uses the provided filters to query the document from the collection and replaces
        all internal fields on the model with the retrieved values.

        :param kwargs filters: MongoDB filter used to locate the current document
        :raises LookupError: If no matching document is found
        """

        new = self.get(**filters).model_dump()
        self.__dict__.update(new)

    # === Deletion ===

    def delete(self):
        """
        Deletes the current document from the database

        Attempts to identify the document using the `_id` field first. If `_id` is not set,
        it falls back to using the `id` field. Raises a `LookupError` if neither identifier
        is available on the current model instance.

        :raises LookupError: If both `_id` and `id` are missing or `None`
        :returns pymongo.results.DeleteResult: Result of the delete operation
        """

        if self._id:
            return self.__collection__.delete_one({"_id": self._id})
        elif hasattr(self, "id") and self.id:
            return self.__collection__.delete_one({"id": self.id})

        raise LookupError("Current document has no identifier (missing both `_id` and `id`)")
