from typing import Any, Dict, Protocol, Sequence, TypeVar


def values_with_discriminator(
    values: Any, discriminator: str, discriminator_value: Any
) -> Dict[str, Any]:
    if isinstance(values, dict):
        values.setdefault(discriminator, discriminator_value)
    return values


class Nameable(Protocol):
    name: str


NameableType = TypeVar("NameableType", bound=Nameable)


def nameables_to_dict(nameables: Sequence[NameableType]) -> Dict[str, NameableType]:
    return {value.name: value for value in nameables}
