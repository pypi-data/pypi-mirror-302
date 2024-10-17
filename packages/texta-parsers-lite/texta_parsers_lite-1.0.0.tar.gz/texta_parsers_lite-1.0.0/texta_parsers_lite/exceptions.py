class ServiceNotAvailableError(Exception):
    """Raised when external service is not available.""" 
    pass

class InvalidInputError(Exception):
    """Raised when something incorrect given to parse."""
    pass

class UnsupportedFileError(Exception):
    """Raised when unsupported file given to parser."""
    pass

class InvalidSplitMethodError(Exception):
    """Raised when TextSplitter is initiated with invalid splitting option."""
    pass
