from string import ascii_letters

from hypothesis import strategies
from sqlalchemy.engine import Dialect

from .hints import Strategy

identifiers_characters = strategies.sampled_from('_' + ascii_letters)
python_identifiers = (strategies.text(alphabet=identifiers_characters,
                                      min_size=1)
                      .filter(str.isidentifier))


def to_sql_identifiers(dialect: Dialect) -> Strategy[str]:
    return strategies.text(alphabet=identifiers_characters,
                           min_size=1,
                           max_size=dialect.max_identifier_length)
