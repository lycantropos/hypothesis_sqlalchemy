from enum import (Enum,
                  EnumMeta)
from typing import (Any,
                    Callable)

from hypothesis import strategies
from sqlalchemy.sql.sqltypes import Enum as EnumType

from .types import Strategy
from .utils import identifiers

ENUM_TEMPLATE = ('class {name}(*bases):\n'
                 '{content}')


# FIXME: find safer way of generating enum
def factory(*,
            names: Strategy = identifiers,
            keys: Strategy = identifiers,
            values: Strategy = strategies.integers(),
            bases: Strategy = strategies.tuples(strategies.just(Enum)),
            value_to_string: Callable[[Any], str] = '{!r}'.format,
            **namespace: Any
            ) -> Strategy:
    contents = strategies.dictionaries(keys=keys,
                                       values=values,
                                       min_size=1)

    def enum_factory(draw: Callable[[Strategy], Any]) -> EnumMeta:
        name = draw(names)
        enum_bases = draw(bases)
        content = draw(contents)
        namespace['bases'] = enum_bases
        indent = 4 * ' '
        lines = (key + '=' + value_to_string(value)
                 for key, value in content.items())
        try:
            content_str = '\n'.join(indent + line
                                    for line in lines)
        except TypeError as err:
            err_msg = ('Invalid strategy: '
                       '"keys" should generate "str" instances.')
            raise ValueError(err_msg) from err
        exec(ENUM_TEMPLATE.format(name=name,
                                  content=content_str),
             namespace)
        return namespace[name]

    return strategies.composite(enum_factory)()


def types_factory(enums: Strategy = factory()) -> Strategy:
    types_values = strategies.one_of(strategies.tuples(enums),
                                     strategies.lists(identifiers,
                                                      min_size=1))

    def enum_type_factory(draw: Callable[[Strategy], Any]) -> EnumType:
        type_values = draw(types_values)
        return EnumType(*type_values)

    return strategies.composite(enum_type_factory)()
