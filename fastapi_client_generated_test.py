
from fastapi_server_with_doc import port # 9982?
CODE = f"""
port = {port}

import sys
client_location ="D:\\project\\xianxing\\chimichang-app-client"

sys.path.append(client_location)

# where's the path?

import chimichang_app_client  as CA
import chimichang_app_client.api.default as DEFAULT
import chimichang_app_client.api.users as USERS
import chimichang_app_client.models as M

breakpoint()
"""
