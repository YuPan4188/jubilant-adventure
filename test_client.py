import requests
import json

port = 3398

with open("test_graph_data.json",'r') as f:
    data = f.read()
    data_dict = json.loads(data)

requests.post(url,)