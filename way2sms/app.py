import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.way2sms.com/"


def _login_check(func):
    """
    A decorator to check if user is logged in or not
    """
    def wrapper(*args):
        """
        Decorator inner method
        """
        if not args[0].logged_in:
            print("Can't perform action since NOT logged in..!")
            return False
        return func(*args)
    return wrapper


class Sms:
    """
    SMS Class
    """

    def __init__(self, mobile_number, password):
        """
        Login with mobile_number and password to create a Session
        """
        self._login_url = BASE_URL + "re-login"
        self._msg_url = BASE_URL + "smstoss"
        self._msg_left_url = BASE_URL + "sentSMS?Token="
        self._future_msg_url = BASE_URL + "schedulesms"
        self._logout_url = BASE_URL + "Logout"
        self._session = requests.Session()
        self._session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"\
                                              "like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        # Do a http GET to get the cookies
        self._session.get(BASE_URL)
        self._session.headers['X-Requested-With'] = 'XMLHttpRequest'
        self._session.headers['Cookie'] = "JSESSIONID=" + self._session.cookies.get_dict()['JSESSIONID']
        payload = {'mobileNo': mobile_number, 'password': password, 'CatType': '', 'redirectPage': '', 'pid': ''}
        response = self._session.post(self._login_url, data=payload)
        if response.status_code == 200 and response.text == "send-sms":
            print("Successfully logged in..!")
            self.logged_in = True
        else:
            print("Can't login, once check credential..!")
            self.logged_in = False
        # JSID is the main KEY and is produced every time a session starts
        self._jsid = self._session.cookies.get_dict()['JSESSIONID'][4:]

    @_login_check
    def msg_sent_today(self):
        """
        Returns number of SMS sent today as there is a limit of 100 messages everyday..!
        """
        response = self._session.get(self._msg_left_url + self._jsid)
        # we want the number of messages sent which is present in the
        soup = BeautifulSoup(response.text, 'html.parser')
        # div element with class "hed" -> h2
        h2_text = soup.find("div", {"class": "hed"}).h2.text
        message_sent_count = 0
        for _ in h2_text:
            if _.isdecimal():
                message_sent_count = 10 * message_sent_count + int(_)
        return message_sent_count

    @_login_check
    def send(self, mobile_number, msg):
        """
        Sends the message to the given mobile number and return boolean
        """
        # checks whether the given message is of length less than equal to 139 and mobile number is valid
        if len(msg) > 139 or len(mobile_number) != 10 or not mobile_number.isdecimal():
            return False
        # I analyzed the NETWORK section in Inspect Element while messaging someone from browser
        payload = {
            'ssaction': 'ss',
            'Token': self._jsid,
            'toMobile': mobile_number,
            'message': msg,
            'sederId': 'WAYSMS'
        }
        response = self._session.post(self._msg_url, data=payload)
        return response.status_code == 200

    @_login_check
    def send_later(self, mobile_number, msg, date, time):
        """
        Function for future SMS feature.
        date must be in dd/mm/yyyy format
        time must be in 24hr format. For ex: 18:05
        """
        if len(msg) > 139 or len(mobile_number) != 10 or not mobile_number.isdecimal():
            return False
        # These steps to check for valid date and time and formatting
        dateparts = date.split('/')
        timeparts = time.split(':')
        if int(dateparts[0]) < 1 or int(dateparts[0]) > 32 or int(dateparts[1]) > 12 or int(dateparts[1]) < 1 or int(
                dateparts[2]) < 2017 or int(timeparts[0]) < 0 or int(timeparts[0]) > 23 or int(
                timeparts[1]) > 59 or int(timeparts[1]) < 0:
            return False
        date = dateparts[0].zfill(2) + "/" + dateparts[1].zfill(2) + "/" + dateparts[2]
        time = timeparts[0].zfill(2) + ":" + timeparts[1].zfill(2)
        payload = {
            'Token': self._jsid,
            'toMobile': mobile_number,
            'sdate': date,
            'stime': time,
            'message': msg
        }
        response = self._session.post(self._future_msg_url, data=payload)
        return response.status_code == 200

    @_login_check
    def logout(self):
        """
        Closes the session and mimics a logout
        """
        self._session.get(self._logout_url)
        self._session.close()
        self.logged_in = False
        print("Successfully logged OUT..!")
