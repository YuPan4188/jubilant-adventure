from fastapi_server_with_doc import port
import requests

baseurl = "http://127.0.0.1:" + port + "/"

url = baseurl + "items"
json_data = dict(name="hello", price=1, is_offer=False, myDict={"mydict": 1})
r = requests.post(url, json=json_data)
