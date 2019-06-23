from hypothesis import strategies
from sqlalchemy.sql.sqltypes import (BigInteger,
                                     Boolean,
                                     Date,
                                     DateTime,
                                     Float,
                                     Integer,
                                     SmallInteger,
                                     String)
from sqlalchemy.sql.type_api import TypeEngine

from hypothesis_sqlalchemy import enums
from hypothesis_sqlalchemy.hints import Strategy


def strings_factory(lengths: Strategy[int] =
                    strategies.integers(min_value=0,
                                        # Postgres VARCHAR max size
                                        max_value=10485760)
                    ) -> Strategy[TypeEngine]:
    return strategies.builds(String,
                             length=lengths)


def primary_keys_factory() -> Strategy[TypeEngine]:
    types = [SmallInteger, Integer, BigInteger]
    return strategies.one_of(*map(strategies.builds, types))


def factory(*,
            string_types: Strategy = strings_factory(),
            enum_types: Strategy = enums.types_factory(),
            primary_keys_types: Strategy = primary_keys_factory()
            ) -> Strategy:
    extra_types = [Float(asdecimal=True), Boolean, Date, DateTime]
    return strategies.one_of(string_types,
                             enum_types,
                             primary_keys_types,
                             strategies.sampled_from(extra_types))
