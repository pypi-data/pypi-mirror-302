# Encoder module for KSON
# Oct 17 2024

from .exceptions import KSONEncodeError

CROWN_EMOJI = '\U0001F451'  # Unicode representation of the crown emoji


def dumps(obj, *, indent=None):
    """
    Serialize obj to a KSON formatted str.

    :param obj: Python object to serialize.
    :param indent: Number of spaces for indentation. Defaults to None.
    :return: KSON string.
    :raises KSONEncodeError: If the object is not serializable.
    """
    encoder = KSONEncoder(indent=indent)
    return encoder.encode(obj)


def dump(obj, fp, *, indent=None):
    """
    Serialize obj as a KSON formatted stream to fp

    :param obj: Python object to serialize.
    :param fp: File-like object with a write() method.
    :param indent: Number of spaces for indentation. Defaults to None.
    :raises KSONEncodeError: If the object is not serializable.
    """
    fp.write(dumps(obj, indent=indent))


class KSONEncoder:
    """
    Encoder class for KSON data.
    """

    def __init__(self, indent=None):
        self.indent = indent

    def encode(self, obj):
        """
        Encode a Python object to a KSON string.

        :param obj: Python object to serialize.
        :return: KSON string.
        :raises KSONEncodeError: If the object is not serializable.
        """
        return self._encode_value(obj, 0)

    def _encode_value(self, obj, level):
        if isinstance(obj, dict):
            return self._encode_object(obj, level)
        elif isinstance(obj, list):
            return self._encode_array(obj, level)
        elif isinstance(obj, str):
            return self._encode_string(obj)
        elif isinstance(obj, (int, float)):
            return self._encode_number(obj)
        elif isinstance(obj, bool):
            return 'true' if obj else 'false'
        elif obj is None:
            return 'null'
        else:
            raise KSONEncodeError(
                f"Object of type {type(obj).__name__} is not KSON serializable"
            )

    def _encode_object(self, obj, level):
        items = []
        indent_str = ' ' * (self.indent * level) if self.indent else ''
        new_level = level + 1
        for key, value in obj.items():
            if not isinstance(key, str):
                raise KSONEncodeError("Keys must be strings")
            key_str = self._encode_string(key)
            value_str = self._encode_value(value, new_level)
            if self.indent is not None:
                item = f'\n{" " * (self.indent * new_level)}{key_str} {CROWN_EMOJI} {value_str}'
            else:
                item = f'{key_str} {CROWN_EMOJI} {value_str}'
            items.append(item)
        if self.indent is not None:
            joined = ','.join(items)
            return f'{{{joined}\n{indent_str}}}'
        else:
            joined = ', '.join(items)
            return f'{{{joined}}}'

    def _encode_array(self, arr, level):
        items = []
        indent_str = ' ' * (self.indent * level) if self.indent else ''
        new_level = level + 1
        for item in arr:
            value_str = self._encode_value(item, new_level)
            if self.indent is not None:
                item_str = f'\n{" " * (self.indent * new_level)}{value_str}'
            else:
                item_str = value_str
            items.append(item_str)
        if self.indent is not None:
            joined = ','.join(items)
            return f'[{joined}\n{indent_str}]'
        else:
            joined = ', '.join(items)
            return f'[{joined}]'

    def _encode_string(self, s):
        if '"' in s:
            s = s.replace('"', '\\"')
        return f'"{s}"'

    def _encode_number(self, num):
        return str(num)
