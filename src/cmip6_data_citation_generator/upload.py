from os.path import isfile, isdir, join
from glob import glob
import json


from netrc import netrc
import httplib2
from httplib2 import Http


def upload_jsons(inputs, test=False):
    if isfile(inputs):
        jsons = [inputs]
    else:
        jsons = glob(join(inputs, "*.json"))

    import pdb

    pdb.set_trace()
    httplib2.debuglevel = 0

    info = netrc()
    http = httplib2.Http()

    login, account, password = info.authenticators("cera")
    http.add_credentials(login, password)

    content_type_header = "application/json"
    url = "http://ceracite.dkrz.de:5000/api/v1/citation"
    if test:
        url = "{}?test=1".format(url)

    for json_file in jsons:
        with open(json_file) as f:
            data = json.load(f)

        response, content = http.request(
            url, "POST", json.dumps(data), headers={"Content-Type": content_type_header}
        )

        print("{}\n{}".format(response.status, content))
