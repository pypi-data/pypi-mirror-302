import requests

class _InternetNotFoundError(Exception):
    pass

class _Internet:
    def __init__(self) -> None:
        response = requests.get("https://www.google.com") # will raise errors if any
        response.raise_for_status() # raises HTTP error
        if response.status_code is not 200:
            raise _InternetNotFoundError("No Internet Connection Found.")