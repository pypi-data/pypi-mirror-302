from eip712.model.schema import EIP712SchemaField, EIP712Type


class MissingRootTypeError(RuntimeError):
    """
    Exception raised when a no root type is found.
    """

    pass


class MultipleRootTypesError(RuntimeError):
    """
    Exception raised when multiple root types are found.
    """

    pass


def get_primary_type(schema: dict[EIP712Type, list[EIP712SchemaField]]) -> EIP712Type:
    """
    Determines the primary type from a given EIP-712 schema.

    The primary type is the root type that is not referenced by any other type in the schema,
    excluding the "EIP712Domain" type. If there are multiple root types or no root type,
    appropriate exceptions are raised.
    """
    referenced_types = {field.type.rstrip("[]") for _, type_fields in schema.items() for field in type_fields}
    match len(roots := set(schema.keys()) - referenced_types - {"EIP712Domain"}):
        case 0:
            raise MissingRootTypeError("Invalid EIP-712 schema: no root type found.")
        case 1:
            return next(iter(roots))
        case _:
            raise MultipleRootTypesError("Invalid EIP-712 schema: multiple root types found.")
