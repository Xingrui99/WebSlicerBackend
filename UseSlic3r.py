from configparser import RawConfigParser
import subprocess
from model.RequestItem import Item

slice_path = r'./Slic3r/Slic3r-console.exe'
output_dir = '.\\output_model\\'
config_path = r'./config/slic3r.ini'


def set_config(item: Item):
    with open(config_path, 'r') as f:
        lines = f.readlines()

    item_dict = item.to_dict()

    for i, line in enumerate(lines):
        key = line.split('=')[0].strip()
        if key in item_dict:
            value=item_dict.get(key)
            lines[i] = f'{key} = {value}\n'

    with open(config_path, 'w') as f:
        f.writelines(lines)


def outputGcode(model_path, export_name, item: Item):
    mm_value = ''
    cm3_value = ''
    set_config(item)
    command_str = f'{slice_path} {model_path} --load {config_path} --output {output_dir}{export_name}.gcode'
    if item.is_support_material:
        command_str = command_str + ' --support-material'
    print(command_str)
    result = subprocess.run(command_str, capture_output=True, text=True)
    print(result)
    if result:
        for line in result.stdout.split('\n'):
            if 'Filament required: ' in line:
                required = line.split(': ')[1].strip()
                mm_value = required.split(' ')[0]
                cm3_value = required.split('(')[1].split(')')[0].strip()
                break
    return mm_value, cm3_value
