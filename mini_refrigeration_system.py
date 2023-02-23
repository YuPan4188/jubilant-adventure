from integratedEnergySystemPrototypes import (
    LiBrRefrigeration,
    CitySupply,
    # no storage?
    # WaterEnergyStorage,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node

# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

cool_load = load.get_cool_load(num_hour0)
delta = 0.3
cool_load = (
    np.array([(1 - delta) + math.cos(i * 0.1) * delta for i in range(len(cool_load))])
    * cool_load
)

model1 = Model(name=simulation_name)

resource = ResourceGet()
municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour0)


# let's add illumination data.

hotWaterLiBr = LiBrRefrigeration(
    num_hour0, model1, LiBr_device_max=10000 * 10000, device_price=1000, efficiency=0.9
)
hotWaterLiBr.constraints_register(model1)


power_highTemperatureHotWater_sum = model1.continuous_var_list(
    [i for i in range(0, num_hour0)], name="power_highTemperatureHotWater_sum"
)

# 市政热水
municipalHotWater = CitySupply(
    num_hour0,
    model1,
    citySupplied_device_max=10000,
    device_price=3000,
    run_price=municipalHotWater_price0,
    efficiency=0.9,
)
municipalHotWater.constraints_register(model1)

model1.add_constraints(
    power_highTemperatureHotWater_sum[h] == municipalHotWater.heat_citySupplied[h]
    for h in range(num_hour0)
)

model1.add_constraints(
    hotWaterLiBr.heat_LiBr_from[h] <= power_highTemperatureHotWater_sum[h]
    for h in range(num_hour0)
)

# consumption and production
model1.add_constraints(
    cool_load[h] == hotWaterLiBr.cool_LiBr[h] for h in range(num_hour0)
)

systems = [hotWaterLiBr,municipalHotWater]

from mini_data_log_utils import solve_and_log

solve_and_log(systems, model1, simulation_name)
