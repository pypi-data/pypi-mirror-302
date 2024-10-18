![](https://cdn.discordapp.com/attachments/1260365923399762021/1279777654966325281/Frame_24.png?ex=66d5ad52&is=66d45bd2&hm=6dbc2843aa21198e1d34c59774bbb04802a53a452355df96b1ebd76ec9206f9c&)

<h1 align="center">StoreJSON</h1>

<p align="center">
StoreJSON is the easiest way to manage data with JSON. It allows you to store, manipulate, and query objects in table form, similar to a database, but with the simplicity and readability of the JSON format. This project is designed to be as accessible as possible while remaining powerful enough for various use cases.
</p>

## Why Use StoreJSON?

- **Simplicity**: With StoreJSON, working with structured data becomes as simple as manipulating Python objects. No complex configuration is needed. Everything is managed through classes.
  
- **Performance**: The use of typed models via [Pydantic](https://docs.pydantic.dev/latest/). enables efficient data validation while ensuring data integrity.

- **Readability**: Storing data in JSON format ensures that your data remains easily readable and modifiable, even without specific tools.

## Example Usage

```python
from storejson import Storage, TableObject

# Create a new storage instance using a JSON file
storage = Storage("./mystorage.json")

# Define a data model for the "users" table
class UserModel(TableObject):
    id: int
    username: str

# Add the "users" table to the storage
User = storage.add_table("users", id_key="id", model_class=UserModel)

# Create a new user and add them to the table
user = User(id=1, username="JohnDoe")
user.storage.push()

# Retrieve a user by their ID
retrieved_user = User.get(1)
print(retrieved_user)

# Update a user
retrieved_user.username = "JaneDoe"
retrieved_user.push()

# Delete a user
retrieved_user.remove()
```

### Using Decorators

If you prefer to use decorators for more concise syntax:

```python
# Create a "users" table using a decorator
@storage.table("users", id_key="id")
class User(TableObject):
    id: int
    username: str

# Create and add a user
user = User(id=2, username="Alice")
user.storage.push()

# Retrieve and display the user
print(User.storage.get(2))
```

## Complete Documentation

To view the full documentation of the project, it is recommended to use `pdoc`.

```bash
pip install pdoc
py -m pdoc storejson
```