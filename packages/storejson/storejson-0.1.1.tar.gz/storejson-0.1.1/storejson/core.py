from typing import (cast, Any, Type, TypeVar, ParamSpec,
                    Generator, Generic, Callable, Generator)
from json import load, dump
from pydantic import BaseModel, PrivateAttr


__all__ = ["Storage", "Table", "TableObject",
           "StorageActions", "NeedIdError"]
ModelT = TypeVar("ModelT", bound="TableObject")
IdT = TypeVar("IdT", str, int)
P = ParamSpec('P')

class NeedIdError(NameError):
    """
    Exception that raise when your trying to
    create an object whithout providing the ID.
    """
    pass



class TableObject(BaseModel):
    """
    Use this class for your Pydantic models instead of BaseModel.
    It adds the obj.storage property to make storage actions.

    **Push the object to the storage**
    >>> obj.storage.push()

    **Edit an object and update**
    >>> obj.code = None
    >>> obj.storage.push()

    **Remove an object from the storage**
    >>> obj.storage.remove()
    """
    _table: "Table" = PrivateAttr(default=None) # type: ignore

    @property
    def object_id(self) -> IdT:
        """
        The ID of the object, standard property instead of using id_key.
        """
        return self.__getattribute__(self._table.id_key)

    @property
    def storage(self) -> "StorageActions":
        """
        The storage actions. Use this to push, update, remove.
        """
        return StorageActions(self)



class StorageActions:
    """
    A bunch of function to manipulate your
    storage on your TableObject instance.
    you're not supposed to construct an instance
    of this class by yourself.
    """
    obj: TableObject
    """
    The table object where the actions will be executed.
    """

    def __init__(self, obj: TableObject) -> None:
        self.obj = obj


    def push(self) -> None:
        """
        Push your object to the storage table.
        Update the object in the storage if the object
        already exists in the storage table.
        """
        existing_obj = self.obj._table.get(self.obj.object_id)
        if existing_obj:
            self.obj._table.update(self.obj)
        else:
            self.obj._table.push(self.obj)


    def remove(self) -> None:
        """
        Remove your object from the storage table.
        """
        self.obj._table.remove(self.obj.object_id)



class Table(Generic[ModelT, P]):
    """
    A database-like table with a typed model
    for its content.

    **Create an object with the model**
    >>> UserTable(id=10278874728859, username="Izak")

    **Load an object from a JSON/dict**
    >>> UserTable.load({"id": 10278874728859, "username": "Izak"})

    **Find objects with filters**
    >>> UserTable.find({"age": 15})
    >>> VerifTable.find({"user_id": user.id})

    **Get object by ID**
    >>> UserTable[10278874728859]
    >>> VerifTable["lawSWkCHDGg"]

    **Update an object that is already in the storage**
    >>> user = UserTable[10278874728859]
    >>> user.username = "NewUsername"
    >>> UserTable.update(obj)
    >>> # you can also use `StorageActions` for this.
    """
    storage: "Storage"
    """
    The storage that the table is on.
    """
    name: str
    """
    The name of the table
    """
    id_key: str
    """
    The JSON key that is used to
    identify the objects of the table.
    """
    model: Type[ModelT]
    """
    The Pydantic model of the table objects.
    """

    def __init__(self,
                 storage: "Storage",
                 name: str,
                 id_key: str,
                 model: Type[ModelT]) -> None:
        """
        Create a table. Please use Storage.table or Storage.add_table
        instead of this constructor.
        """
        self.storage = storage
        self.name = name
        self.id_key = id_key
        self.model = model


    def __call__(self, *args: P.args, **fields: P.kwargs) -> ModelT:
        """
        Create your object.
        Litteraly a proxy of the constructor of your model.
        """
        return self.load(fields)


    def load(self, data: dict[str, Any]) -> ModelT:
        """
        Load the object with the data.
        Litteraly a proxy of `YourModel.model_validate`.
        """
        obj = self.model.model_validate(data)
        obj._table = self

        if not self.id_key in obj.model_dump():
            raise NeedIdError(
                "The object u tryna construct need an ID dawg how we supposed to locate your object. "
                f"ID key for table {self.name!r}: {self.id_key!r}"
            )

        return obj


    def push(self, obj: ModelT) -> None:
        """
        Push your object to the storage table.
        """
        table_data = self.storage._read_table(self.name)

        if self.get(obj.object_id):
            raise ValueError(f"Object with id {obj.object_id!r} already exists in table {self.name}")

        table_data.append(obj.model_dump())
        self.storage._write_table(self.name, table_data)


    def find(self, filters: dict[str, Any]) -> Generator[ModelT, None, None]:
        """
        Find all the objects in the table that
        are matching with the filters.
        """
        table_data = self.storage._read_table(self.name)
        for item in table_data:
            if all(item.get(key) == value for key, value in filters.items()):
                yield self.load(item)


    def get(self, id: IdT) -> ModelT | None:
        """
        Get the object that owns the ID you provided.
        Returns None if the object you lookin for
        is unknown.
        """
        return next(self.find({self.id_key: id}), None)


    def remove(self, id: IdT) -> None:
        """
        Remove your object from the storage table.
        """
        table_data = self.storage._read_table(self.name)
        new_table_data = [item for item in table_data if item.get(self.id_key) != id]
        self.storage._write_table(self.name, new_table_data)


    def update(self, obj: ModelT) -> None:
        """
        Update your object in the table with the older one.
        "same objects" refer as `obj1.object_id == obj2.object_id`
        """
        table_data = self.storage._read_table(self.name)
        for index, item in enumerate(table_data):
            if item.get(self.id_key) == obj.object_id:
                table_data[index] = obj.model_dump()
                break
        else:
            raise ValueError(f"Object with id {id} not found in table {self.name}")
        self.storage._write_table(self.name, table_data)


    __getitem__ = get




class Storage:
    """
    A file storage that work with JSON
    and that is the easiest human readable storage.

    **Create a storage**
    >>> storage = Storage("./mystorage.json")

    **Create a table with decorator**

    NOTE: using decorator, VSCode/Mpypy will not pass the typecheck
    and you will not have the auto-completion or type hinting.
    see https://github.com/python/mypy/issues/3135
    >>> @storage.table("users", id_key="id")
    ... class User(TableObject):
    ...     id: int
    ...     username: str

    **Create a table without decorator**
    >>> class User(TableObject):
    ...     id: int
    ...     username: str
    ...
    >>> storage.add_table("users", id_key="id", model_class=User)
    """
    file_path: str | None
    """
    The path of the JSON storage file.
    """
    tables: list[Table]
    """
    Available loaded tables.
    """

    def __init__(self, file_path: str | None) -> None:
        """
        Create the storage. The file can be non-existent, we will
        create it if it's needed.
        If the file_path is None, the database will be ephemeral and stored in the RAM.
        """
        self.file_path = file_path
        self.tables = []
        self._ephe = {}


    def table(self,
              name: str,
              id_key: str) -> Callable[[Callable[P, ModelT]], Table[ModelT, P]]:
        """
        Define a Pydantic model as a model for a table and create the table.
        Need to be used as decorator.
        """
        def decorator(klass):
            table = Table(self, name, id_key, klass)
            self.tables.append(table)
            return table
        return decorator


    def add_table(self,
                  name: str,
                  id_key: str,
                  model_class: Callable[P, ModelT]) -> Table[ModelT, P]:
        """
        Same as `.table` method but without decorator.
        """
        table = Table(self, name, id_key, cast(Type[ModelT], model_class))
        self.tables.append(table)
        return table


    def _read_data(self) -> dict:
        if not self.file_path:
            return self._ephe

        try:
            with open(self.file_path, 'r') as f:
                return load(f)
        except:
            self._write_data({})
            return self._read_data()


    def _write_data(self, data: dict) -> None:
        if not self.file_path:
            self._ephe = data
            return

        with open(self.file_path, 'w') as f:
            dump(data, f, indent=4)


    def _read_table(self, table_name: str) -> list[dict]:
        data = self._read_data()
        return data.get(table_name, [])


    def _write_table(self, table_name: str, table_data: list[dict]) -> None:
        data = self._read_data()
        data[table_name] = table_data
        self._write_data(data)