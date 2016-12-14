# Way2Sms

Send upto 100 free [SMS](http://site24.way2sms.com/content/index.html) within 10 seconds daily.

[Way2Sms](http://site24.way2sms.com/content/index.html) provides free SMS service upto **100** messages daily with message length upto **139**. 

```python
import way2sms
```
-  Login

  ```python
q=login.sms(username,password)
  ```
- Send SMS, returns True if sent

  ```python
  q.send(mobile_number,message)
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
 
 
### Todos

 - Future Message
 
**Free Messaging, Hell Yeah!**
