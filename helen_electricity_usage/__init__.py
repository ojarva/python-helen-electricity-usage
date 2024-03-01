from datetime import datetime, timezone, timedelta
from typing import Optional
import json
import logging
import requests
import sys
import xml.etree.ElementTree as ET


class Helen:
    def __init__(self, username: str, password: str, delivery_site_id: int, session: requests.Session = None) -> None:
        """ Api Client to communicate with Helen portal API

        :param str username: Helen portal username. Usually email address
        :param str password: The users password to Helen portal
        :param int delivery_site_id: Helen delivery site id user has access to
        :param requests.Session session: Requests session to use. If not provided one will be created
        """
        self.username = username
        self.password = password
        self.delivery_site_id = delivery_site_id
        self.session = requests.Session() if session is None else session
        self.access_token = None
        self.login_url = None
        self.log = logging.getLogger('HelenApiClient')

    def _parse_js_redirect_form(self, content: str) -> tuple:
        """ Parse JS based redirect from <noscript> forms in Helen login flow.

        :param str content: Page HTML as string
        :return: Tuple containing form action url, code and state
        :rtype: tuple[str]
        """
        root = ET.fromstring(content)
        form = root.find(".//{http://www.w3.org/1999/xhtml}form[@action][@id='form']")
        action = form.get("action")
        self.log.debug("Parsed return URL from form as '%s'" % action)
        code = form.find(".//{http://www.w3.org/1999/xhtml}input[@name='code']")
        state = form.find(".//{http://www.w3.org/1999/xhtml}input[@name='state']")
        if state is None or code is None:
            raise Exception("Something went wrong while parsing state and code")
        return (action, code.get("value"), state.get("value"))

    def scrape_login_url(self) -> str:
        """ Scrape Helen login page for the actual openid login URL.

        The URL to Helen login contains OpenID client and application IDs that change from request to request.
        Start from the TupasLoginFrame to dig for the required URL for login.

        :return: the URL to login to Helen Oma portal
        :rtype: str
        """
        login_host = "login.helen.fi"

        # Start by getting TupasLoginFrame (UI entrypoint for login)
        res = self.session.get("https://www.helen.fi/hcc/TupasLoginFrame?service=account&locale=fi")
        self.log.debug("TupasLoginFrame response status: %s", res.status_code)
        res.raise_for_status()

        # find login form address from the TupasLoginFrame
        res_element = ET.fromstring(res.text)
        form = res_element.findall(".//form[@action]")
        login_form_url = form[0].get("action")
        self.log.debug("Login form is at '%s'", login_form_url)

        # Get the login form
        res = self.session.post(login_form_url)
        self.log.debug("login_form_url response status: %s", res.status_code)
        res.raise_for_status()

        # Find the authorization endpoint from the login form
        res_element = ET.fromstring(res.text)
        form = res_element.findall(".//{http://www.w3.org/1999/xhtml}form[@action]")
        self.login_url = f"https://{login_host}{form[0].get('action')}"
        self.log.info("Login url is '%s'", self.login_url)

        return self.login_url

    def login(self, login_url: Optional[str] = None) -> None:
        """ Log in to Helen portal and return the authorization token

        :param str login_url: Override for the one time login URL
        """
        if login_url is None:
            login_url = self.scrape_login_url() if self.login_url is None else self.login_url

        res = self.session.post(login_url, data={"username": self.username, "password": self.password})
        if res.status_code != 200:
            raise Exception("Login failed. Most likely unauthorized")

        # After successful login one needs to click on a button to continue or let the js do it for you.
        action, code, state = self._parse_js_redirect_form(res.text)

        # Use the parsed url and params to continue
        res = self.session.get(action, params={"code": code, "state": state})
        if res.status_code != 200:
            raise Exception("Something went wrong with login :(")

        # Hard coded manual redirect from https://www.helen.fi/authResponse
        res = self.session.get("https://api.omahelen.fi/v2/login", params={"redirect": "https://web.omahelen.fi/?lang=fi", "lang": "fi"})

        # Continue with new code and state.
        action, code, state = self._parse_js_redirect_form(res.text)
        res = self.session.get(action, params={"code": code, "state": state})

        self.access_token = self.session.cookies.get("accessToken")

    def get_electricity(self, begin: datetime, end: datetime, resolution: str = "hour", allow_transfer: bool = True) -> dict:
        """ Get Electricity consumption metrics from Helen API

        The metrics are usually delayed for a day or so.

        :param datetime begin: Time to start the electricity report from. Aware datetime with UTC timezone
        :param datetime end: Time to end the electricity report to. Aware datetime with UTC timezone
        :param str resolution: The resolution or size of buckets in the report.
        :param bool allow_transfer: Unknown upstream parameter.
        :return: dictionary response from Helen API
        :rtype: dict
        """
        if self.access_token is None:
            raise Exception("Invalid state: Helen must be logged in before calling get_electricity()")

        res = self.session.get(
            "https://api.omahelen.fi/v8/measurements/electricity",
            params={
                "begin": begin.isoformat(timespec="seconds").replace("+00:00", "Z"),
                "end": end.isoformat(timespec="seconds").replace("+00:00", "Z"),
                "resolution": resolution,
                "delivery_site_id": self.delivery_site_id,
                "allow_transfer": allow_transfer,
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json"
            }
        )
        return res.json()


def main(args):
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

    if len(args) != 3:
        print("Mandatory parameters: username password delivery_site_id")
        return 2

    helen = Helen(username=args[0], password=args[1], delivery_site_id=args[2])
    helen.login()

    print("Requesting electricity report")
    now = datetime.now(tz=timezone.utc)
    one_day = timedelta(days=1)
    yesterday = now - one_day
    begin = yesterday.replace(hour=0, minute=0, second=0)
    end = yesterday.replace(hour=23, minute=59, second=59)
    print(json.dumps(helen.get_electricity(begin, end), indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
