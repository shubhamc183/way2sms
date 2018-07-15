import requests
from bs4 import BeautifulSoup


#".*//"
class Sms:

	def __init__(self, mobileNo, password):

		'''
		Takes mobileNo and password as parameters for constructors and try to log in
		'''

		self.base_url = "http://www.way2sms.com/"
		self.login_url = self.base_url + "re-login"
		self.msg_url=  self.base_url + "smstoss"
		self.future_msg_url = self.base_url + "schedulesms"
		self.logout_url = self.base_url + "Logout"

		self.session = requests.Session()	# Session because we want to maintain the cookies
		self.session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
		self.session.get(self.base_url)		# once do a http GET to get the cookies       

		#self.session.headers['Referer'] = self.base_url
		#self.session.headers['Host'] = self.base_url
		self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
		#self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
		#self.session.headers['Content-Length'] = '43'
		self.set_cookies_header()

		self.payload = {'mobileNo': mobileNo, 'password': password, 'CatType' : ''}
		self.q = self.session.post(self.login_url, data=self.payload)		# POST the payload
		self.logged_in = False				# a variable of knowing whether logged in or not

		if self.q.status_code == 200 and self.q.text == "send-sms":	# http status 200 == OK
			print("Successfully logged in..!")
			self.logged_in=True
		else:
			print("Can't login, once check credential..!")
			self.logged_in=False

		self.jsid = self.session.cookies.get_dict()['JSESSIONID'][4:]	    # JSID is the main KEY as JSID are produced every time a session satrts

	def set_cookies_header(self):
		self.session.headers['Cookie'] = "JSESSIONID=" + self.session.cookies.get_dict()['JSESSIONID']

	def msgSentToday(self):

		'''
		Returns number of SMS sent today as there is a limit of 100 messages everyday..!
		'''

		if self.logged_in == False:
			print("Can't perform since NOT logged in..!")
			return -1

		self.msg_left_url='http://www.way2sms.com/sentSMS?Token='+self.jsid
		self.q=self.session.get(self.msg_left_url)
		self.soup=BeautifulSoup(self.q.text,'html.parser')		#we want the number of messages sent which is present in the
		self.t=self.soup.find("div",{"class":"hed"}).h2.text		# div element with class "hed" -> h2
		self.sent=0

		for self.i in self.t:
			if self.i.isdecimal():
				self.sent=10*self.sent+int(self.i)
		return self.sent

	def send(self,mobile_no,msg):

		'''
		Sends the message to the given mobile number
		'''

		if self.logged_in == False:
			print("Can't perform since NOT logged in..!")
			return False

		if len(msg)>139 or len(mobile_no)!=10 or not mobile_no.isdecimal():	#checks whether the given message is of length more than 139 and mobile numnber is valid
			return False							

		self.payload = {
						'ssaction':'ss',
						'Token':self.jsid,					#inorder to visualize how I came to these payload,
			        	'toMobile':mobile_no,			#must see the NETWORK section in Inspect Element
       				 	'message':msg,						#while messagin someone from your browser
       			    }

		self.q=self.session.post(self.msg_url,data=self.payload)

		if self.q.status_code==200 and self.q.text == '0':
			return True
		else:
			return False

	def send_later(self, mobile_no, msg, date, time):				#Function for future SMS feature.
											#date must be in dd/mm/yyyy format
											#time must be in 24hr format. For ex: 18:05

		if self.logged_in == False:
			print("Can't perform since NOT logged in..!")
			return False
		
		if len(msg)>139 or len(mobile_no)!=10 or not mobile_no.isdecimal():
			return False

		dateparts = date.split('/')			#These steps to check for valid date and time and formatting
		timeparts = time.split(':')
		if int(dateparts[0])<1 or int(dateparts[0])>32 or int(dateparts[1])>12 or int(dateparts[1])<1 or int(dateparts[2])<2017 or int(timeparts[0])<0 or int(timeparts[0])>23 or int(timeparts[1])>59 or int(timeparts[1])<0:
			return False
		date = dateparts[0].zfill(2) + "/" + dateparts[1].zfill(2) + "/" + dateparts[2]
		time = timeparts[0].zfill(2) + ":" + timeparts[1].zfill(2)

		self.payload = {'Token' : self.jsid,
						'toMobile' : mobile_no,
						'sdate' : date,
						'stime' : time,
						'message' : msg,
					}

		self.q = self.session.post(self.future_msg_url, data=self.payload)
		if self.q.status_code == 200:
			return True
		else:
			return False

	def logout(self):
		self.session.get(self.logout_url)
		self.session.close()								# close the Session
		self.logged_in=False
