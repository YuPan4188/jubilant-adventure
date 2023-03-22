sources_curl_get = dict(optim="cloudpss_optim.mjson", simu="cloudpss_simu.mjson")
# almost the same as `cloudpss_config2.py`, with slight alternation.
choice = "simu"

param_translate_maps = dict(
    optim=dict(参数分类=[], 中文名称=[], 有关设备=[]), simu=dict(参数分类=[], 中文名称=[], 有关设备=[])
)


mjson_path = sources_curl_get[choice]

import json
import pandas as pd

# question: convert pandas dataframe to markdown table.
headliner = lambda level: "#" * level

with open(mjson_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

level_shift = 0

existing_keys = []
for line in lines:
    try:
        data = json.loads(line.strip())
        param = data["ele"]["param"]
        key_prefix = name = param["name"]

        if key_prefix not in existing_keys:
            existing_keys.append(key_prefix)

            print()
            print(headliner(level_shift + 2), key_prefix)
            print()

            pin = [v for _, v in param["pin"].items()]  # iterate through keys.
            pin_df = pd.DataFrame(pin)
            print(headliner(level_shift + 3), "针脚定义")
            print()
            print(pin_df.to_markdown())
            # you can also get conditional pins and connection types.
            existing_keys = []

            print()
            print(headliner(level_shift + 3), "参数填写")
            # shall create this table for every device.
            params = param["param"]
            input_types = list(params.keys())
            for input_type in input_types:
                component_info = []
                input_data = params[input_type]
                for k, v in input_data["params"].items():
                    valDict = {"ID": k}
                    valDict.update({k0: v0 for k0, v0 in v.items()})
                    component_info.append(valDict)

                df = pd.DataFrame(component_info)
                print()
                print(headliner(level_shift + 4), input_type)
                print()
                markdown_table = df.to_markdown(index=False)
                print(markdown_table)
        print()
    except:
        # obviously we've hit something hard.
        continue
