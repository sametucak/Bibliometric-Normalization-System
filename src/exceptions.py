"""
Custom exceptions for the Bibliometric Normalization System (BNS).
"""


class BNSError(Exception):
    """Base exception for all BNS errors."""
    pass


class ValidationError(BNSError):
    """Raised when input data validation fails."""
    pass


class SimilarityError(BNSError):
    """Raised when similarity calculation fails."""
    pass


class MergeError(BNSError):
    """Raised when record merging fails."""
    pass


class ExportError(BNSError):
    """Raised when exporting results fails."""
    pass

