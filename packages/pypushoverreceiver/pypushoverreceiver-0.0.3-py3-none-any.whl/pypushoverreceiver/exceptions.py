"""Hyyp Api Exceptions."""


class PushoverApiError(Exception):
    """Pushover api exception."""


class InvalidURL(PushoverApiError):
    """Invalid url exception."""


class HTTPError(PushoverApiError):
    """Invalid host exception."""
