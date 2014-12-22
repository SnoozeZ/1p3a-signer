#coding=gbk 
#Developed by Snooze, 2014-12-18
import requests
import re
import time
####
username = "snooze"
password = "7efd42209ac34abcb13a07069cd88fe4"  #password in 32-md5 here
blabla = 'Little hand one shake, big rice arrive hand.' #your blabla here
###

def getTime():
  while True:
    try:
      r = requests.get('http://www.1point3acres.com/bbs/')
      break;
    except Exception,ex:
      print Exception,":",ex
      time.sleep(1)
  date = r.headers['date']
  hour = (int(date[17:19]) + 8) % 24 #GMT -> Chinese time zone
  minute = int(date[20:22])
  second = int(date[23:25])
  return {'h':hour, 'm':minute, 's':second}

def login():
  my_info = []
  #get cookie
  login_data = {'username': username, 
    'password': password, 
    'quickforward': 'yes', 
    'handlekey': 'ls'}
  while True:
    try:
      r = requests.post("http://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",
        data = login_data)
      break;
    except Exception,ex:
      print Exception,":",ex
      time.sleep(1)
  my_info.append(r.cookies)
  
  #find the odd WTF "formhash"
  while True:
    try:
      r = requests.post("http://www.1point3acres.com/bbs/",
        cookies = my_info[0])
      break
    except Exception,ex:
      print Exception,":",ex
      time.sleep(1)    
  pattern = 'formhash=.*?&'
  formhash = re.findall(pattern,r.content,re.S)[0][9:17]
  my_info.append(formhash)
  
  return my_info

  
def sign(my_info):
  #SIGN NOW!
  sign_data = {'formhash': my_info[1], 
    'qdxq': 'fd', 
    'qdmode': '1', 
    'todaysay': blabla,
    'fastreply': '0'}
  while True:
    try:
      r = requests.post("http://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1",
        data = sign_data,
        cookies = my_info[0])
      break
    except Exception,ex:
      print Exception,":",ex
      time.sleep(1)
      
  if r.content.find("萝卜") != -1:
    print 'Successfully signed! -3-'
    return False
  else:
    print 'Failed! - -#'
    return True
  
if __name__ == "__main__":
  while 1:
    tmp = getTime() #get the 1p3a server's time
    if tmp['h'] < 23 or tmp['m'] < 29:
      print "Sleeping... 1p3a's current time "+str(tmp['h'])+":"+str(tmp['m'])+":"+str(tmp['s'])
      time.sleep(1620)
    else:
      my_info = login()
      slptm = (59 - tmp['m']) * 60 + (59 - tmp['s'])
      print "It's comming... I will sleep " +str(slptm-10)+ " seconds."
      time.sleep(slptm - 10)
      for i in range(100):
        print "Try " +str(i)+" times, your local time is " + str(time.strftime('%H:%M:%S',time.localtime(time.time())))
        if sign(my_info):
          continue
        else:
          break
