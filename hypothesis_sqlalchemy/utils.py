from string import ascii_letters

from hypothesis import strategies
from sqlalchemy.engine import Dialect

from hypothesis_sqlalchemy.hints import Strategy

identifiers_characters = strategies.sampled_from('_' + ascii_letters)


def to_sql_identifiers(dialect: Dialect) -> Strategy[str]:
    max_size = dialect.max_identifier_length
    min_size = min(8, max_size)
    return strategies.text(alphabet=identifiers_characters,
                           min_size=min_size,
                           max_size=max_size)


python_identifiers = (strategies.text(alphabet=identifiers_characters,
                                      min_size=1)
                      .filter(str.isidentifier))
