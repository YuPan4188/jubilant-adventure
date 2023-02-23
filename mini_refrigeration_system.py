
from integratedEnergySystemPrototypes import LiBrRefrigeration, CitySupply, WaterEnergyStorage
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node
# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
cool_load = load.get_cool_load(num_hour0)

model1 = Model(name=simulation_name)

resource = ResourceGet()
municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour0)



hotWaterLiBr = LiBrRefrigeration(
    num_hour0, model1, LiBr_device_max=10000*10000, device_price=1000, efficiency=0.9
)
hotWaterLiBr.constraints_register(model1)

model1.add_constraint(hotWaterLiBr.heat_LiBr_from[h] == )

# consumption and production
model1.add_constraint(cool_load[h] == hotWaterLiBr.cool_LiBr[h] for h in range(num_hour0))