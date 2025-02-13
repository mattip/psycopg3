"""
psycopg3 -- PostgreSQL database adapter for Python
"""

# Copyright (C) 2020-2021 The Psycopg Team

import logging

from . import pq
from . import types
from .copy import Copy, AsyncCopy
from .adapt import global_adapters
from .cursor import AnyCursor, AsyncCursor, Cursor
from .errors import Warning, Error, InterfaceError, DatabaseError
from .errors import DataError, OperationalError, IntegrityError
from .errors import InternalError, ProgrammingError, NotSupportedError
from ._column import Column
from .conninfo import ConnectionInfo
from .connection import BaseConnection, AsyncConnection, Connection, Notify
from .transaction import Rollback, Transaction, AsyncTransaction
from .server_cursor import AsyncServerCursor, ServerCursor

from .dbapi20 import BINARY, DATETIME, NUMBER, ROWID, STRING
from .dbapi20 import Binary, BinaryTextDumper, BinaryBinaryDumper
from .dbapi20 import Date, DateFromTicks, Time, TimeFromTicks
from .dbapi20 import Timestamp, TimestampFromTicks

from .version import __version__

# Set the logger to a quiet default, can be enabled if needed
logger = logging.getLogger("psycopg3")
if logger.level == logging.NOTSET:
    logger.setLevel(logging.WARNING)

# register default adapters
types.register_default_globals(global_adapters)

# DBAPI compliancy
connect = Connection.connect
apilevel = "2.0"
threadsafety = 2
paramstyle = "pyformat"
BinaryTextDumper.register(Binary, global_adapters)  # dbapi20
BinaryBinaryDumper.register(Binary, global_adapters)  # dbapi20


# Note: defining the exported methods helps both Sphynx in documenting that
# this is the canonical place to obtain them and should be used by MyPy too,
# so that function signatures are consistent with the documentation.
__all__ = [
    "__version__",
    "AnyCursor",
    "AsyncConnection",
    "AsyncCopy",
    "AsyncCursor",
    "AsyncServerCursor",
    "AsyncTransaction",
    "BaseConnection",
    "Column",
    "Connection",
    "Copy",
    "Cursor",
    "Notify",
    "Rollback",
    "ServerCursor",
    "Transaction",
    # DBAPI exports
    "connect",
    "apilevel",
    "threadsafety",
    "paramstyle",
    "Warning",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgrammingError",
    "NotSupportedError",
]
