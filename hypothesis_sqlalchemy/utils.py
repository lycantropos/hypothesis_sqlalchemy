from string import ascii_letters

from hypothesis import strategies
from sqlalchemy.schema import Column

# more info at:
# for PostgreSQL
# https://www.postgresql.org/docs/current/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
# for MySQL
# https://dev.mysql.com/doc/refman/en/identifiers.html
MAX_IDENTIFIER_LENGTH = 63

identifiers_characters = strategies.sampled_from('_' + ascii_letters)
sql_identifiers = strategies.text(alphabet=identifiers_characters,
                                  min_size=8,
                                  max_size=MAX_IDENTIFIER_LENGTH)
python_identifiers = (strategies.text(alphabet=identifiers_characters,
                                      min_size=1)
                      .filter(str.isidentifier))


def is_column_unique(column: Column) -> bool:
    return column.unique or column.primary_key
