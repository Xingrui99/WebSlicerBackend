from fastapi import FastAPI, File, UploadFile
import CalculateMaterialService
import CalculateTimeService
from model.RequestItem import Item
import uvicorn

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('WebSlicerBackend:app', host='127.0.0.1', port=8000, reload=False)


@app.get('/api/hello')
def hello():
    return {'msg': 'hello'}


@app.post('/api/calculate')
async def calculate(electricity_price: float,
                    is_support_material: bool = False,
                    perimeter_speed: float = 60,
                    small_perimeter_speed: float = 15,
                    external_perimeter_speed: str = '50%',
                    infill_speed: float = 80,
                    solid_infill_speed: float = 20,
                    top_solid_infill_speed: float = 15,
                    gap_fill_speed: float = 20,
                    bridge_speed: float = 60,
                    support_material_speed: float = 60,
                    travel_speed: float = 130,
                    first_layer_speed: float = 30,
                    file: UploadFile = File(...),
                    ):
    item = Item(is_support_material=is_support_material, perimeter_speed=perimeter_speed,
                small_perimeter_speed=small_perimeter_speed, external_perimeter_speed=external_perimeter_speed,
                infill_speed=infill_speed, solid_infill_speed=solid_infill_speed,
                top_solid_infill_speed=top_solid_infill_speed, gap_fill_speed=gap_fill_speed,
                bridge_speed=bridge_speed, support_material_speed=support_material_speed, travel_speed=travel_speed,
                first_layer_speed=first_layer_speed)
    result1 = await CalculateMaterialService.get_material_cost(item, file)
    pla_cost, petg_cost, abs_cost, output_filename = result1
    result2 = await CalculateTimeService.start_process(output_filename)
    hours = result2
    electricity_cost = hours * electricity_price

    msg={
        'pla_cost':pla_cost,
        'petg_cost':petg_cost,
        'abs_cost':abs_cost,
        'gcode_filename':output_filename,
        'print_time':hours,
        'electricity_cost':electricity_cost,
        'pla_total_cost':pla_cost+electricity_cost,
        'petg_total_cost':petg_cost+electricity_cost,
        'abs_total_cost':abs_cost+electricity_cost
    }
    return msg


@app.post('/api/getTimeCost')
async def get_time_cost(file_name):
    result = await CalculateTimeService.start_process(file_name)
    return {'time': result}
