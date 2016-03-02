from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import json
import requests
import sys
import time


class Helen(object):

    def __init__(self, username, password, metering_point_number, customer_number):
        self.username = username
        self.password = password
        self.metering_point_number = metering_point_number
        self.customer_number = customer_number
        self.session = requests.Session()
        self.session_time = int(time.time() * 1000)

    def login(self):
        resp = self.session.get("https://www2.helen.fi/mobiili/")
        loginpage = BeautifulSoup(resp.text, "html.parser")
        post_url = "https://login.helen.fi" + loginpage.find("div", "loginitem").find("form").get("action")
        resp = self.session.post(post_url, data={"username": self.username, "password": self.password})
        authpage = BeautifulSoup(resp.text, "html.parser")
        loginform = authpage.find("div", "loginbutton").find("form")
        shibboleth_url = loginform.get("action")
        post_data = {}
        for item in loginform.find_all("input"):
            if item.get("name") is None:
                continue
            post_data[item.get("name")] = item.get("value")

        login_page = self.session.post(shibboleth_url, data=post_data)

    def get_session_time(self):
        self.session_time += 1
        return self.session_time

    def get_date(self, date):
        response = self.session.get("https://www2.helen.fi/api/meteringpoints/0/%s/series?enddate=%s&numberofmonths=12&numberofyears=2&resolution=DAYS_AS_HOURS&selector=value,status,day,month,year,hour,milestones(title,note,timestamp(date,month,year)),temperature,prediction,telePrediction,budget,teleEuro,waterFlowPrice" % (self.metering_point_number, date), auth=('%s/MainUserElec' % self.customer_number, 'N/A'))
        if response.status_code != 200:
            raise ValueError("Server returned %s" % response.status_code)
        if len(response.history) > 0:
            raise ValueError("Request was redirected. Probably authorization issue - is metering point number set properly?")
        try:
            return json.loads(response.text)
        except:
            print (response.text)
            raise ValueError("Unable to parse response JSON")


def main(args):
    if len(args) != 4:
        print("Mandatory parameters: username password metering_point_number customer_number")
        return 2
    helen = Helen(args[0], args[1], args[2], args[3])
    helen.login()
    print((helen.get_date("20151204")))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
