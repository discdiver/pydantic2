# The Field function is used to customize and add metadata to model fields
# Default values

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(default="John Doe")


user = User()
print(user)


# JSON Schema generation with nested models
import json
from enum import Enum

from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class FooBar(BaseModel):
    count: int
    size: float | None = None


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    not_given = "not_given"


class MainModel(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title="Main")

    foo_bar: FooBar
    gender: Annotated[Gender | None, Field(alias="Gender")] = None
    snap: int = Field(
        42,
        title="The Snap",
        description="this is the value of snap",
        gt=30,
        lt=50,
    )


main_model_schema = MainModel.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!

# This produces a "jsonable" dict of MainModel's schema.
# Calling json.dumps on the schema dict produces a JSON string.
# What does this output remind you of? - Hint: something in the Prefect world.

# can customize the JSON schema output with the json_schema_extra option at filed and/or model level
# with Field or model_config

# Field customization with json_schema_extra has built in parameters such as title, description, examples.
import json

from pydantic import BaseModel, EmailStr, Field, SecretStr


class User(BaseModel):
    age: int = Field(description="Age of the user")
    email: EmailStr = Field(examples=["marcelo@mail.com"])
    name: str = Field(title="Username")
    password: SecretStr = Field(
        json_schema_extra={
            "title": "Password",
            "description": "Password of the user",
            "examples": ["123456"],
        }
    )


print(json.dumps(User.model_json_schema(), indent=2))

# Built-in JSON parsing
# fast(esp. in Pydantic 2.5 and greater), custom erros, strict specs possible
from datetime import date

from pydantic import BaseModel, ConfigDict, ValidationError


class Event(BaseModel):
    model_config = ConfigDict(strict=True)

    when: date
    where: tuple[int, int]


json_data = '{"when": "1987-01-28", "where": [51, -1]}'
print(Event.model_validate_json(json_data))
# > when=datetime.date(1987, 1, 28) where=(51, -1)

try:
    Event.model_validate({"when": "1987-01-28", "where": [51, -1]})
except ValidationError as e:
    print(e)

# Should see 2 validation errors - why?


# Serialization
# Convert a model to a JSON-encoded string or a dictionary

# model_dump() method
print(user.model_dump())
print(type(user.model_dump()))

# model_dump_json() method
print(user.model_dump_json())
print(type(user.model_dump_json()))

# Note the different output types

# Serialization generally, and serialization of nested models specifically, is a whole thing.
# See the docs for the details: https://docs.pydantic.dev/latest/concepts/serialization/
