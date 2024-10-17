# Exceptions for the KSON module.
# Oct 17 2024

class KSONDecodeError(ValueError):
    """Exception raised for errors in the decoding process."""
    pass


class KSONEncodeError(TypeError):
    """Exception raised for errors in the encoding process."""
    pass
