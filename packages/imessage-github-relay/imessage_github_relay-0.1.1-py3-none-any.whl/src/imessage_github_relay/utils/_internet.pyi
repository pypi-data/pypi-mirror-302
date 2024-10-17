import requests

class _InternetNotFoundError(Exception):
    """`No Internet Connection Error Exception`"""
    ...

class _Internet:
    """`Internet Connection Check handler class.`
    
    Internal Class of `iMessage GitHub Relay`.
    """
    ...
    def __init__(self) -> None:
        """`Tries to check if internet connection is present by pinging to google.com`."""
        ...