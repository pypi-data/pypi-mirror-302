"""
kson - A Python library for parsing and serializing KSON data.

KSON is a custom data format similar to JSON but uses the crown emoji
as the key-value separator.

Modules exported by this package:

- loads: Deserialize KSON to a Python object.
- dumps: Serialize a Python object to KSON.
- load: Deserialize KSON from a file-like object.
- dump: Serialize a Python object to KSON and write to a file-like object.
"""

from .decoder import load, loads
from .encoder import dump, dumps
from .exceptions import KSONDecodeError

__all__ = ["load", "loads", "dump", "dumps", "KSONDecodeError"]

__version__ = "0.0.1"
