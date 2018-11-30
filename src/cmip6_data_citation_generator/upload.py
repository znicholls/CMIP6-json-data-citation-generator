from os.path import isfile, join
from glob import glob
import json


from netrc import netrc
from httplib2 import Http


def upload_jsons(inputs, test=False):
    if isfile(inputs):
        jsons = [inputs]
    else:
        jsons = glob(join(inputs, "*.json"))

    info = netrc()
    http = Http()

    login, account, password = info.authenticators("cera")
    http.add_credentials(login, password)

    content_type_header = "application/json"
    url = "http://ceracite.dkrz.de:5000/api/v1/citation"

    errors = False
    if test:
        print("Would upload the following files to:\n{}".format(url))
    for json_file in jsons:
        if test:
            print("    - {}".format(json_file))
            continue
        with open(json_file) as f:
            data = json.load(f)

        response, content = http.request(
            url, "POST", json.dumps(data), headers={"Content-Type": content_type_header}
        )
        content = content.decode("utf-8")
        print("{}, {}".format(response.status, content))

        errors = errors or not content.startswith("SUCCESS")

    return 1 if errors else 0
