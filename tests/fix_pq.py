import sys

import pytest

from .utils import check_libpq_version


def pytest_report_header(config):
    try:
        from psycopg import pq
    except ImportError:
        return []

    return [
        f"libpq available: {pq.version()}",
        f"libpq wrapper implementation: {pq.__impl__}",
    ]


def pytest_configure(config):
    # register libpq marker
    config.addinivalue_line(
        "markers",
        "libpq(version_expr): run the test only with matching libpq"
        " (e.g. '>= 10', '< 9.6')",
    )


def pytest_runtest_setup(item):
    from psycopg import pq

    for m in item.iter_markers(name="libpq"):
        assert len(m.args) == 1
        msg = check_libpq_version(pq.version(), m.args[0])
        if msg:
            pytest.skip(msg)


@pytest.fixture
def libpq():
    """Return a ctypes wrapper to access the libpq."""
    import ctypes.util

    try:
        # Not available when testing the binary package
        if sys.platform == "win32":
            libname = ctypes.util.find_library("libpq.dll")
        else:
            libname = ctypes.util.find_library("pq")
        assert libname, "libpq libname not found"
        if sys.implementation.name == "pypy" and not hasattr(ctypes, "pydll"):
            # PyPy issue 3496
            # https://foss.heptapod.net/pypy/pypy/-/issues/3496
            # does this work "close enough"?
            return ctypes.cdll.LoadLibrary(libname)
        else:
            return ctypes.pydll.LoadLibrary(libname)
    except Exception as e:
        from psycopg import pq

        if pq.__impl__ == "binary":
            pytest.skip(f"can't load libpq for testing: {e}")
        else:
            raise
