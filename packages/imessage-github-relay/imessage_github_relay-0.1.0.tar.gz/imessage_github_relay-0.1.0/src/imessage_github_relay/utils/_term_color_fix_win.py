from colorama import Fore as cf
import requests
import sys

class _GitHubFile:
    def __init__(self, filename: str = "cmd_color_fix.bat", username: str = 'd33p0st', repository: str = 'iMessage-github-relay', branch: str = 'main') -> None:
        self.url = f"https://raw.githubusercontent.com/{username}/{repository}/refs/heads/{branch}/{filename}"
        self.filename = filename

    @property
    def contents(self) -> str:
        try:
            response = requests.get(self.url)

            try:
                response.raise_for_status()
            except Exception as e:
                print(f"{cf.RED}Error{cf.RESET}: Exception occured while trying to get {self.filename} from GitHub: {e}")
                sys.exit(1)
            
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"{cf.RED}Error{cf.RESET}: Exception occured while trying to get {self.filename} from GitHub: {e}")