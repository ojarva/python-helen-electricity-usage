import requests
import time
import datetime
import json
import sys

class Helen(object):

    def __init__(self, username, password, metering_point_number):
        self.username = username
        self.password = password
        self.metering_point_number = metering_point_number
        self.session = requests.Session()
        self.session_time = int(time.time() * 1000)

    def login(self):
        self.session.get("https://www2.helen.fi/mobiili/login.jsp")
        self.session.post("https://www2.helen.fi/mobiili/j_spring_security_check", data={"j_username": "%s;;ENERGY;FIN" % self.username, "j_password": self.password})
        response = self.session.get("https://www2.helen.fi/mobiili/app/index.html")
        if response.status_code != 200:
            raise ValueError("Login failed.")
        if len(response.history) > 0:
            raise ValueError("Login failed.")

    def get_session_time(self):
        self.session_time += 1
        return self.session_time

    def get_date(self, date):
        response = self.session.get("https://www2.helen.fi/mobiili/meteringpoints/ELECTRICITY/%s/series?resolution=DAYS_AS_HOURS&numberofyears=1&numberofmonths=12&selector=value,hour,day,month,year,milestones(title,note,timestamp(date,month,year))&enddate=%s&_=%s" % (self.metering_point_number, date, self.get_session_time()))
        if response.status_code != 200:
            raise ValueError("Server returned %s" % response.status_code)
        if len(response.history) > 0:
            raise ValueError("Request was redirected. Probably authorization issue - is metering point number set properly?")
        return json.loads(response.text)

def main(args):
    if len(args) != 3:
        print("Mandatory parameters: username password metering_point_number")
        return 2
    helen = Helen(args[0], args[1], args[2])
    helen.login()
    print((helen.get_date("20141226")))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
