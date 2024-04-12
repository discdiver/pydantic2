#  _Unset, typing.optional, None, Annotated, **EmptyKwargs
# Enum, Literal,

# Union
# Validating with Union is tricky, see the docs if you need to do this https://docs.pydantic.dev/latest/concepts/unions/


# validate_call is a decorator - super easy (new name since V1)


from pydantic import ValidationError, validate_call


@validate_call
def repeat(s: str, count: int, *, separator: bytes = b"") -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


a = repeat("hello", 3)
print(a)


b = repeat("x", "4", separator=b" ")
print(b)


try:
    c = repeat("hello", "wrong")
except ValidationError as exc:
    print(exc)
