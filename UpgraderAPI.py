import requests
from bs4 import BeautifulSoup

class UpgraderAPI:
    @staticmethod
    def _headers():
        return {
            # text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.6",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # content length is added later
            "origin": "https://upgrader.cc",
            "referer": "https://upgrader.cc/info.php",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

    @staticmethod
    def get_key_info(key: str) -> dict:

        url = "https://upgrader.cc/info.php"

        headers = UpgraderAPI._headers()
        headers["content-length"] = str(len(key))

        form = {
            "key": key
        }

        session = requests.Session()
        response = session.post(url, headers=headers, data=form)
        soup = BeautifulSoup(response.text, "html.parser")
        lis = soup.find_all("li")
        
        key_data = {
            "status"    : None,
            "last_use"  : None,
            "usable"    : None,
            "address"   : None
        }

        for li in lis:
            text = li.text
            if text.startswith("STATUS: "):
                key_data["status"] = text.replace("STATUS: ", "")
            elif text.startswith("LAST USE: "):
                key_data["last_use"] = text.replace("LAST USE: ", "")
            elif text.startswith("USABLE: "):
                key_data["usable"] = text.replace("USABLE: ", "")
            elif text.startswith("ADDRESS: "):
                key_data["address"] = text.replace("ADDRESS: ", "")
        
        return key_data

    @staticmethod
    def upgrade_account(
        key: str,
        username: str,
        password: str,
        country: str="US",
    ) -> str:
        url = "https://upgrader.cc/upgrade.php"

        headers = UpgraderAPI._headers()
        headers["content-length"] = str(len(key))

        form = {
            "key": key,
            "usr": username,
            "pwd": password,
            "country": country
        }

        session = requests.Session()
        response = session.post(url, headers=headers, data=form)
    
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        # grid__item grid__item--padding
        div = soup.find("div", {"class": "grid__item grid__item--padding"})
        # find UL -> LI get text
        li = div.find("ul").find("li")
        return li.text
    
    @staticmethod
    def renew_key(
        key: str,
        username: str,
        password: str,
    ) -> str:
        url = "https://upgrader.cc/renew.php"

        headers = UpgraderAPI._headers()
        headers["content-length"] = str(len(key))

        form = {
            "key": key,
            "usr": username,
            "pwd": password
        }

        session = requests.Session()
        response = session.post(url, headers=headers, data=form)

        response_text = response.text
        # pares
        soup = BeautifulSoup(response_text, "html.parser")
        # grid__item grid__item--padding
        div = soup.find("div", {"class": "grid__item grid__item--padding"})
        # find UL -> LI get text
        li = div.find("ul").find("li")
        return li.text
