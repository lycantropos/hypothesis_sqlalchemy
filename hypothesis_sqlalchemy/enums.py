import enum
from typing import (Any,
                    Callable)

from hypothesis import strategies
from sqlalchemy.sql.sqltypes import Enum

from .types import Strategy
from .utils import identifiers

ENUM_TEMPLATE = ('class {name}(*bases):\n'
                 '{content}')


# FIXME: find safer way of generating enum
def factory(*,
            names: Strategy = identifiers,
            keys: Strategy = identifiers,
            values: Strategy = strategies.integers(),
            bases: Strategy = strategies.tuples(strategies.just(enum.Enum)),
            value_to_string: Callable[[Any], str] = '{!r}'.format,
            **namespace: Any
            ) -> Strategy:
    def enum_factory(draw: Callable[[Strategy], Any]) -> enum.EnumMeta:
        name = draw(names)
        enum_bases = draw(bases)
        contents = strategies.dictionaries(keys=keys,
                                           values=values,
                                           min_size=1)
        content = draw(contents)
        namespace['bases'] = enum_bases
        indent = 4 * ' '
        lines = (key + '=' + value_to_string(value)
                 for key, value in content.items())
        content_str = '\n'.join(indent + line
                                for line in lines)
        exec(ENUM_TEMPLATE.format(name=name,
                                  content=content_str),
             namespace)
        return namespace[name]

    return strategies.composite(enum_factory)()


def types_factory(enums: Strategy = factory()) -> Strategy:
    def enum_type_factory(draw: Callable[[Strategy], Any]) -> Enum:
        types_values = strategies.one_of(strategies.tuples(enums),
                                         strategies.lists(identifiers,
                                                          min_size=1))
        type_values = draw(types_values)
        return Enum(*type_values)

    return strategies.composite(enum_type_factory)()
