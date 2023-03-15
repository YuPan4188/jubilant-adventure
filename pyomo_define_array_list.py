##在Pyomo中，可以使用以下方式定义数组和变量组：
##1. 定义数组：可以使用Python中的列表（list）或Numpy中的数组（array）定义数组，然后使用pyomo.environ.Param组件定义Pyomo中的参数。例如，定义一个包含10个元素的数组，可以使用以下代码：
import numpy as np
from pyomo.environ import *

# 定义数组
arr = np.arange(10)
# 定义参数
model = ConcreteModel()
model.A = Param(range(10), initialize={i: arr[i] for i in range(10)}, units=units.meter)


##2. 定义变量组：可以使用pyomo.environ.Set组件定义变量组，并使用pyomo.environ.Var组件定义变量。例如，定义一个包含10个变量的变量组，可以使用以下代码：
# 定义变量组
model.I = Set(initialize=range(10))
# 定义变量
model.x = Var(model.I, initialize=0)
##在上述代码中，我们定义了一个变量组I，其中包含10个变量，然后使用pyomo.environ.Var组件定义了一个变量x，它是变量组I中的每个变量。


def objective(self):
    return sum(model.I[i] * model.A[j] for i in range(10) for j in range(10))


model.OBJ = Objective(rule=objective)
solver = SolverFactory("cbc")
results = solver.solve(model)
model.I.display()