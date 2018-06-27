import sys
import netrc
import httplib2
import json

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print "please provide a JSON as the first parameter"
    sys.exit(1)
  data = {}
  with open(sys.argv[1]) as data_file:
    data = json.load(data_file)
  extra_param = ""
  if len(sys.argv) == 3 and sys.argv[2] == "test":
    extra_param = "?test=1"

  info = netrc.netrc()
  login, account, password = info.authenticators("cera")
  httplib2.debuglevel     = 0
  http                    = httplib2.Http()
#, disable_ssl_certificate_validation=True)
  content_type_header     = "application/json"
  url = "http://ceracite.dkrz.de:5000/api/v1/citation"+extra_param;
#  url = "http://afast-laptop.d.dkrz.de:5000/api/v1/citation"+extra_param;
#  auth = base64.encodestring( login + ':' + password )
  http.add_credentials(login, password)

  headers = {'Content-Type': content_type_header}
  response, content = http.request( url,
                                    'POST',
                                    json.dumps(data),
                                    headers=headers)
  print response.status, content
