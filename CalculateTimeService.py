import re
import asyncio


def parse_code_value(cmd_line, code):
    if code in cmd_line:
        pattern = r'{}(\d+(\.\d+)?)'.format(code)
        match = re.search(pattern, cmd_line)
        if match:
            value = float(match.group(1))
            return value, True
    return None, False


def calculate(file_path):
    with open(file_path, 'r') as f:
        cmd_lines = f.readlines()

    print_time = 0
    speed = 1
    prev_status = {'x': 0, 'y': 0, 'z': 0, 'e': 0}

    is_coordinates_relative = False
    is_extrusion_relative = False

    for cmd_line in cmd_lines:
        cmds = cmd_line.split()
        if cmds:
            cmd_code = cmds[0].upper()
        else:
            continue
        x_moved = 0
        y_moved = 0
        z_moved = 0
        e_moved = 0
        distance = 0
        layer_print_time = 0
        extrusion_time = 0
        move_time = 0
        if cmd_code == 'M82':
            is_extrusion_relative = False
        if cmd_code == 'M83':
            is_extrusion_relative = True
        if cmd_code == 'G90':
            is_coordinates_relative = False
        if cmd_code == 'G91':
            is_coordinates_relative = True
        if cmd_code == 'G92':
            x, is_x_exist = parse_code_value(cmd_line, 'X')
            y, is_y_exist = parse_code_value(cmd_line, 'Y')
            z, is_z_exist = parse_code_value(cmd_line, 'Z')
            e, is_e_exist = parse_code_value(cmd_line, 'E')
            if is_x_exist:
                prev_status['x'] = x
            if is_y_exist:
                prev_status['y'] = y
            if is_z_exist:
                prev_status['z'] = z
            if is_e_exist:
                prev_status['e'] = e
        if cmd_code == 'G1':
            x, is_x_exist = parse_code_value(cmd_line, 'X')
            y, is_y_exist = parse_code_value(cmd_line, 'Y')
            z, is_z_exist = parse_code_value(cmd_line, 'Z')
            e, is_e_exist = parse_code_value(cmd_line, 'E')
            f, is_f_exist = parse_code_value(cmd_line, 'F')
            if is_f_exist:
                speed = f
            if is_coordinates_relative:
                x_moved = x if is_x_exist else 0
                y_moved = y if is_y_exist else 0
                z_moved = z if is_z_exist else 0
                if is_x_exist:
                    prev_status['x'] += x
                if is_y_exist:
                    prev_status['y'] += y
                if is_z_exist:
                    prev_status['z'] += z
            else:
                x_moved = x - prev_status['x'] if is_x_exist else 0
                y_moved = y - prev_status['y'] if is_y_exist else 0
                z_moved = z - prev_status['z'] if is_z_exist else 0
                if is_x_exist:
                    prev_status['x'] = x
                if is_y_exist:
                    prev_status['y'] = y
                if is_z_exist:
                    prev_status['z'] = z
            if is_extrusion_relative:
                e_moved = e if is_e_exist else 0
                if is_e_exist:
                    prev_status['e'] += e
            else:
                e_moved = e - prev_status['e'] if is_e_exist else 0
                if is_e_exist:
                    prev_status['e'] = e
            abs_e_moved = abs(e_moved)
            if abs_e_moved > 0:
                extrusion_time = abs_e_moved / speed
            distance = (x_moved ** 2 + y_moved ** 2 + z_moved ** 2) ** 0.5
            move_time = distance / speed
            layer_print_time = max(move_time, extrusion_time)
            print_time += layer_print_time

    print(f'总共需耗时:{print_time}分钟')
    return print_time/60


async def start_process(file_name):
    file_path = r'.\output_model\{}.gcode'.format(file_name)
    print_time = await asyncio.to_thread(calculate, file_path)
    return print_time
