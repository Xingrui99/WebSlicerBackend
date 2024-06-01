class PrintMaterial:
    def __init__(self,name:str,density:float,price:float):
        self.name=name
        self.density=density
        self.price=price
    def get_name(self)->str:
        return self.name
    def get_density(self)->float:
        return self.density
    def get_price(self)->float:
        return self.price

PLA=None
PETG=None
ABS=None

def init_materials():
    global PLA,PETG,ABS
    PLA = PrintMaterial(name='PLA', density=1.23, price=0.03)
    PETG = PrintMaterial(name='PETG', density=1.27, price=0.04)
    ABS = PrintMaterial(name='ABS', density=1.21, price=0.035)

init_materials()