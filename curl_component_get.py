template_paths = dict(
    optim="curl_optim_component_get.sh.j2", simu="curl_simu_component_get.sh.j2"
)

id_paths = dict(
    optim="cloudpss_component_optimize_ports.json",
    simu="cloudpss_component_ports.json"
)
import json

def get_ids(id_path:str):
    with open(id_path) as f:
        data = json.loads(f.read())
        cmp = data['cmp']
        for component in cmp:
            
ids = {key: get_ids(val) for key, val in id_paths.items()}

import jinja2
from jinja2 import StrictUndefined
import subprocess

output_script_path = "script.sh"

cmd = ['bash', output_script_path, ]
access_paths = ['CPS','Heat']

for template_path in template_paths:
    with open(template_path,'r', encoding='utf-8') as f:
        source = f.read()
        template = jinja2.Template(source = source, undefined=StrictUndefined)
        script_content = template.render(access_path=access_path, id=_id)
        with open(output_script_path, 'w+') as f0:
            f0.write(script_content)