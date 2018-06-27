# python 2.6+ required or 2.5 plus simplejson
import sys
import netrc
import urllib2,base64
try:
    import json
except ImportError:
    import simplejson as json 
#import simplejson as json
#import json
import time
import datetime

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print "please provide a JSON as the first parameter"
    sys.exit(1) 
  data = {}
  with open(sys.argv[1]) as data_file:
      data = json.load(data_file)
  #data_file = open(sys.argv[1])
  #data = json.load( data_file )
  extra_param = ""
  if len(sys.argv) == 3 and sys.argv[2] == "test":
    extra_param = "?test=1"

  info = netrc.netrc()
  login, account, password = info.authenticators("cera")
  content_type_header     = "application/json"
  #url = "http://afast-laptop.d:5000/api/v1/citation"
  #url = "http://lobstertest.dkrz.de:5000/api/v1/citation"
  url = "http://ceracite.dkrz.de:5000/api/v1/citation"+extra_param

  headers = {'Content-Type': content_type_header}
  request = urllib2.Request(url=url,headers=headers,data=json.dumps(data))
  base64string = base64.b64encode('%s:%s' % (login, password))
  request.add_header("Authorization", "Basic %s" % base64string) 
  try:
      response = urllib2.urlopen(request)
      print (response.code,response.read())
  except urllib2.HTTPError, e:
      print (e.code,e.read())
