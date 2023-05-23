class CrawlerError(Exception):
    """
    Base exception class for all crawler-related exceptions.
    """


class UnknownTaskType(CrawlerError):
    """
    Raised when Iob does not know what to do
    with some objects received from generator.
    """


class RequestConfigurationError(CrawlerError):
    """
    Raised when Request object is instantiating with
    invalid parameters.
    """
