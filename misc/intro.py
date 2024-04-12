# 1. Pydantic model schema creation and validation
# A Pydantic model is a class that inherits from Pydantic's BaseModel class.

from datetime import datetime
from pydantic import BaseModel


class Delivery(BaseModel):
    timestamp: datetime
    dimensions: tuple[int, int]


m = Delivery(timestamp="2020-01-02T03:04:05Z", dimensions=["10", "20"])
print(m.timestamp)
print(repr(m.timestamp))
print(type(m.timestamp))


print(m.dimensions)


# What just happened here?

# Hint, note what got passed in and what came out
# Automatic type coercion - like Prefect gives you (b/c we use Pydantic)

# Uncomment this and run it:
# m = Delivery(timestamp="2020-01-02T03:04:05Z", dimensions=["z", "20"])

# Why did that happen?

# Basemodel is super common in Pydantic.
# It's a way to define a schema for your data.


from datetime import datetime

from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    "id": 123,
    "signup_ts": "2019-06-01 12:22",
    "tastes": {
        "wine": 9,
        b"cheese": 7,  # bytes literal - Pydantic schema expects a string, so coerces to regular string
        "cabbage": "1",
    },
}

print(external_data)
user = User(
    **external_data
)  # Note that you need to unpack the dictionary here for instantiation of the User object

print(user)

print(user.model_dump())  # Different method than Pydantic v1

# Note the difference between the output of print(user) and print(user.model_dump())
# Why is the latter in order when the former is unlikely to be?


print(user.id)

# Uncomment this and run it:
# print(external_data.id)

# Note the difference between how to refer to the fields of the User object and the fields of the external_data dictionary
