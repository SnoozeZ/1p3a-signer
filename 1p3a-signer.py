#coding=gbk 
#Developed by Snooze, 2014-12-18
import requests
import re
import time
import thread
####
username = "snooze"
password = "7efd42209ac34abcb13a07069cd88fe5"  #password in 32-md5 here
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
  my_cookies = r.cookies
  
  #find the odd WTF "formhash"
  while True:
    try:
      r = requests.post("http://www.1point3acres.com/bbs/",
        cookies = my_cookies)
      break
    except Exception,ex:
      print Exception,":",ex
      time.sleep(1)    
  pattern = 'formhash=.*?&'
  formhash = re.findall(pattern,r.content,re.S)[0][9:17]
  my_info = (my_cookies, formhash)
  
  return my_info

  
def sign(cookies, formhash):
  #SIGN NOW!
  sign_data = {'formhash': formhash, 
    'qdxq': 'fd', 
    'qdmode': '1', 
    'todaysay': blabla,
    'fastreply': '0'}
  #while True:
  try:
    r = requests.post("http://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1",
      data = sign_data,
      cookies = cookies)
    #break
  except Exception,ex:
    print Exception,":",ex
    #time.sleep(1)
      
  if r.content.find("ÂÜ²·") != -1:
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
      print "It's comming... I will sleep " +str(slptm-4)+ " seconds."
      time.sleep(slptm-4)
      for i in range(40):
        print "Try " +str(i)+" times, your local time is " + str(time.strftime('%H:%M:%S',time.localtime(time.time())))
        thread.start_new_thread(sign, my_info)
        time.sleep(0.2) 
        #if sign(my_info):
        #  continue
        #else:
        #  break
