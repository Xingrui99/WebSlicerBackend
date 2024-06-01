from pathlib import Path
import os
import uuid
import UseSlic3r
import asyncio
from fastapi import File, UploadFile
from model import PrintMaterial
from model.RequestItem import Item

INPUT_PATH = '.\\input_model'


def calculate_material_cost(volume_str: str, density: float, price: float) -> float:
    volume = float(volume_str[:-3])
    cost = volume * density * price
    print(cost)
    return round(cost, 2)


# 获得材料体积
async def get_material_volume_service(item: Item, file):
    # 生成唯一文件名
    new_filename = str(uuid.uuid4()) + '_' + file.filename
    # 判断上传目录是否存在
    Path(INPUT_PATH).mkdir(parents=True, exist_ok=True)
    # 文件存储路径
    file_path = os.path.join(INPUT_PATH, new_filename)
    # 写入文件
    with open(file_path, 'wb+') as f:
        contents = await file.read()
        f.write(contents)
    # 导出文件名
    output_filename = new_filename.split('.')[0]
    result = await asyncio.to_thread(UseSlic3r.outputGcode, file_path, output_filename, item)
    mm, cm3 = result
    return mm, cm3, output_filename


async def get_material_cost(item: Item, file: UploadFile = File(...)):
    mm, cm3, output_filename = await get_material_volume_service(item, file)
    print('mm:' + mm)
    print('cm3:' + cm3)
    pla_cost = calculate_material_cost(cm3, PrintMaterial.PLA.get_density(), PrintMaterial.PLA.get_price())
    petg_cost = calculate_material_cost(cm3, PrintMaterial.PETG.get_density(), PrintMaterial.PETG.get_price())
    abs_cost = calculate_material_cost(cm3, PrintMaterial.ABS.get_density(), PrintMaterial.ABS.get_price())
    return pla_cost, petg_cost, abs_cost,output_filename
