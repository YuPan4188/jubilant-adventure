url_optim = lambda page: f'https://ies.cloudpss.net:8201/editor/componentheatList/?page={page}'
url_simul = lambda page: f'https://ies.cloudpss.net:8202/editor/componentheatList/?page={page}'

headers = {
    'authority': 'ies.cloudpss.net:8202',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cookie': 'first=1; theme=default; csrftoken=3FDpA3heSB6cmzwGFwUstfQ7PBCMjXi8fyhyOdAGEKlRDBCgS5n0xTLtRg3dqWF7; first=1; theme=default; TK=4e128a76808f4e283cb57df7d3fd098e18c91354; username=Steven0128; email=; id=1197; setlang=test; setlang1=test213; SECKEY_ABVK=V2LDA8s7CsTqpEEHZq0kunbrSZIbVUyBKuZLzkxV+vw%3D; BMAP_SECKEY=Gn9oAOjImVjpMeGQEOuqu-zE2PUFOpAlR0LOJUXUUmQkP5Nkqu-6wpuNDgbgk1mXXjumQhwk7yBTOiU-jHcWek_wLf9N8O3r2yss8J30VnEmuhyI2HR7aJsENkDqXayJ8W5qBUpZNx4ZXmCRabQpy15Rc0cFryLOVOB7VhKJ3qqIErNMIjvaToW7irv6Anss; csrf=y44LdL8zKAS5ekFb0juN8AQIT4sUFULlm6zyM7COSOVS2zCiYTtJGTl7xNmg5s5r; csrftoken=y44LdL8zKAS5ekFb0juN8AQIT4sUFULlm6zyM7COSOVS2zCiYTtJGTl7xNmg5s5r; sessionid=mqn7ewz4kiayaun1ztsde5vfnrxg1udl',
  'referer': 'https://ies.cloudpss.net:8202/editor/?id=21559',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

import requests

r = requests.get(url_optim(1), headers=headers)
print(r.content)