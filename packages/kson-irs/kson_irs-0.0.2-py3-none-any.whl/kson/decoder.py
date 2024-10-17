# Decoder module for KSON
# Oct 17 2024

import re
from .exceptions import KSONDecodeError

CROWN_EMOJI = '\U0001F451'  # Unicode representation of the crown emoji


def loads(s):
    """
    Deserialize s (a str instance containing a KSON document)
    to a Python object.

    :param s: KSON string.
    :return: Python object.
    :raises KSONDecodeError: If the data is invalid.
    """
    decoder = KSONDecoder()
    return decoder.decode(s)


def load(fp):
    """
    Deserialize fp (a file-like object containing a KSON document)
    to a Python object.

    :param fp: File-like object with a read() method.
    :return: Python object.
    :raises KSONDecodeError: If the data is invalid.
    """
    return loads(fp.read())


class KSONDecoder:
    """
    Decoder class for KSON data.
    """

    def __init__(self):
        self.s = ''
        self.len = 0
        self.idx = 0

    def decode(self, s):
        """
        Decode a KSON string to a Python object.

        :param s: KSON string.
        :return: Python object.
        :raises KSONDecodeError: If the data is invalid.
        """
        self.s = s
        self.len = len(s)
        self.idx = 0
        value = self._parse_value()
        self._skip_whitespace()
        if self.idx != self.len:
            raise KSONDecodeError(f"Extra data at position {self.idx}")
        return value

    def _parse_value(self):
        self._skip_whitespace()
        if self.idx >= self.len:
            raise KSONDecodeError("Unexpected end of KSON input")
        char = self.s[self.idx]
        if char == '{':
            return self._parse_object()
        elif char == '[':
            return self._parse_array()
        elif char == '"':
            return self._parse_string()
        elif char.isdigit() or char == '-':
            return self._parse_number()
        elif self.s.startswith('true', self.idx):
            self.idx += 4
            return True
        elif self.s.startswith('false', self.idx):
            self.idx += 5
            return False
        elif self.s.startswith('null', self.idx):
            self.idx += 4
            return None
        else:
            raise KSONDecodeError(f"Invalid value at position {self.idx}")

    def _parse_object(self):
        obj = {}
        self.idx += 1  # Skip '{'
        self._skip_whitespace()
        if self.idx < self.len and self.s[self.idx] == '}':
            self.idx += 1
            return obj
        while True:
            self._skip_whitespace()
            if self.idx >= self.len or self.s[self.idx] != '"':
                raise KSONDecodeError(
                    f"Expecting property name enclosed in double quotes at position {self.idx}"
                )
            key = self._parse_string()
            self._skip_whitespace()
            if not self.s.startswith(CROWN_EMOJI, self.idx):
                raise KSONDecodeError(
                    f"Expecting crown emoji '{CROWN_EMOJI}' after key at position {self.idx}"
                )
            self.idx += len(CROWN_EMOJI)  # Skip crown emoji
            self._skip_whitespace()
            value = self._parse_value()
            obj[key] = value
            self._skip_whitespace()
            if self.idx >= self.len:
                raise KSONDecodeError("Unexpected end of KSON input")
            if self.s[self.idx] == ',':
                self.idx += 1
                continue
            elif self.s[self.idx] == '}':
                self.idx += 1
                break
            else:
                raise KSONDecodeError(
                    f"Expecting ',' or '}}' at position {self.idx}"
                )
        return obj

    def _parse_array(self):
        arr = []
        self.idx += 1  # Skip opening '['
        self._skip_whitespace()
        if self.idx < self.len and self.s[self.idx] == ']':
            self.idx += 1
            return arr
        while True:
            value = self._parse_value()
            arr.append(value)
            self._skip_whitespace()
            if self.idx >= self.len:
                raise KSONDecodeError("Unexpected end of KSON input")
            if self.s[self.idx] == ',':
                self.idx += 1
                continue
            elif self.s[self.idx] == ']':
                self.idx += 1
                break
            else:
                raise KSONDecodeError(
                    f"Expecting ',' or ']' at position {self.idx}"
                )
        return arr

    def _parse_string(self):
        self.idx += 1  # Skip opening '"'
        start = self.idx
        result = ''
        while self.idx < self.len:
            char = self.s[self.idx]
            if char == '"':
                result = self.s[start:self.idx]
                self.idx += 1  # Skip closing '"'
                return result
            elif char == '\\':
                raise KSONDecodeError(
                    f"Escape sequences are not supported at position {self.idx}"
                )
            self.idx += 1
        raise KSONDecodeError(f"Unterminated string starting at position {start}")

    def _parse_number(self):
        start = self.idx
        if self.s[self.idx] == '-':
            self.idx += 1
        while self.idx < self.len and self.s[self.idx].isdigit():
            self.idx += 1
        if self.idx < self.len and self.s[self.idx] == '.':
            self.idx += 1
            if self.idx >= self.len or not self.s[self.idx].isdigit():
                raise KSONDecodeError(
                    f"Expecting digit after decimal point at position {self.idx}"
                )
            while self.idx < self.len and self.s[self.idx].isdigit():
                self.idx += 1
        num_str = self.s[start:self.idx]
        try:
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            raise KSONDecodeError(f"Invalid number at position {start}")

    def _skip_whitespace(self):
        while self.idx < self.len and self.s[self.idx] in ' \t\n\r':
            self.idx += 1
