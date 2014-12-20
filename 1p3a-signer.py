#coding=gbk 
#Developed by Snooze, 2014-12-18

import requests
import re
import time
####
username = "snooze"
password = "7efd42209ac34abcb13a07069cd88fe4"  #32-cmd here
blabla = 'Little hand one shake, big rice arrive hand.' #your blabla here
###

def getTime():
  r = requests.get('http://www.1point3acres.com/bbs/')
  date = r.headers['date']
  hour = (int(date[17:19]) + 8) % 24 #GMT -> Chinese time zone
  minute = int(date[20:22])
  second = int(date[23:25])
  return {'h':hour, 'm':minute, 's':second}

def login():
  login_data = {'username': username, 
    'password': password, 
    'quickforward': 'yes', 
    'handlekey': 'ls'}
  r = requests.post("http://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",
    data = login_data)
  my_cookies = r.cookies
  return r.cookies

  
def sign(my_cookies):
  #find the odd "formhash"
  r = requests.get("http://www.1point3acres.com/bbs/",
    cookies = my_cookies)
  pattern = 'formhash=.*?&'
  formhash = re.findall(pattern,r.content,re.S)[0][9:17]
  #SIGN NOW!
  sign_data = {'formhash': formhash, 
    'qdxq': 'fd', 
    'qdmode': '1', 
    'todaysay': blabla,
    'fastreply': '0'}
  r = requests.post("http://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1",
    data = sign_data,
    cookies = my_cookies)
  if r.content.find("请明天再来") != -1:
    print r.content
    return False
  else:
    print r.content
    return True
  


if __name__ == "__main__":
  while 1:
    print 123321
    tmp = getTime() #get the 1p3a sever's time
    print 123321
    if tmp['h'] != 23 | tmp['m'] < 29:
      print "Sleeping... 1p3a's current time "+str(tmp['h'])+":"+str(tmp['m'])+":"+str(tmp['s'])
      #time.sleep(1620)
    #else:
      my_cookies = login()
      slptm = (59 - tmp['m']) * 60 + (59 - tmp['s'])
      print "It's comming... I will sleep " +str(slptm-10)+ " seconds."
      #time.sleep(slptm - 10)
      for i in range(100):
        print "Try " +str(i)+" times, your local time is " + str(time.strftime('%H:%M:%S',time.localtime(time.time())))
        if sign(my_cookies):
          continue
        else:
          break
