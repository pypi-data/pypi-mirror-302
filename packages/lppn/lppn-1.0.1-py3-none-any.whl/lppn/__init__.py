from .lppn import get
# _version.py must not be tracked by git for 'setuptools_scm' to do it's job.
# This means it might not be available for unittest. It is not tested anyway,
# so it's optional.
try:
    from ._version import (
        __version__,
        version,
        __version_tuple__,
        version_tuple,
        VERSION_TUPLE,
    )
except ModuleNotFoundError:
    pass
