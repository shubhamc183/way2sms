# Way2Sms

Send upto 100 free [SMS](http://site24.way2sms.com/content/index.html) within 10 seconds daily.

[Way2Sms](http://site24.way2sms.com/content/index.html) provides free SMS service upto **100** messages daily with message length upto **139**. 

Either be in same directory or add this file in python path..!
```python
import way2sms
```
-  Login

  ```python
q=way2sms.sms(username,password)
  ```
- Send SMS, returns True if sent

  ```python
  q.send( 'mobile_number', 'message' )      # both are STRING
  ```
- Message Sent today, returns the number

 ```python
 q.msgSentToday()
 ```
- Logout

 ```python
 q.logout()
 ```
 
#Python3 and Packages

 * Install Python3

 ```sh
$ sudo apt-get python3
```

 * Install pip

 ```sh
$ sudo apt-get install python3-pip
```

 * Requests
  
 ```sh
 $ sudo pip3 install requests
 ```
 * BeautifulSoup
 
 ```sh
 $ sudo pip3 install beautifulsoup4
 ```
 
 

Future Message added by [AbdHan](https://github.com/abdhan)
 
**Free Messaging, Hell Yeah!**
