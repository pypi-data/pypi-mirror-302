from colorama import Fore as cf
import requests
import sys

class _GitHubFile:
    """`GitHub File Content Fetcher class`
    
    Internal Class of `iMessage GitHub Relay`.
    """
    def __init__(self, filename: str = "cmd_color_fix.bat", username: str = 'd33p0st', repository: str = 'iMessage-github-relay', branch: str = 'main') -> None:
        """`Create a _GitHubFile object.`
        
        #### Parameters
        - **`filename`**: The filename of the file to be fetched.
        - **`username`**: The username of the repository owner.
        - **`repository`**: The GitHub repository name.
        - **`branch`**: The branch of the repository where the file exists.
        """
        ...
    
    @property
    def contents(self) -> str:
        """`Returns the contents of the _GitHubFile if exists and no errors found. Else exits with error.`"""
        ...