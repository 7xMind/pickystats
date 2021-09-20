class InvalidItemTypeError(Exception):
    """
    Raised when the item extracted from text file does not conform
    to the assumptions and thus, cannot be normalized.
    """