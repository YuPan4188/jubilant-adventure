from pydantic import BaseModel
from pyomo.environ import *
from dataclasses import dataclass

model = ConcreteModel()

@dataclass
class 环境:
    温度: float  # (°C)
    空气比湿度: float  # (kg/kg)
    太阳辐射强度: float  # (W/m2)
    土壤平均温度: float  # (°C)
    距地面10m处东向风速: float  # (m/s)
    距地面50m处东向风速: float  # (m/s)
    距地面10m处北向风谏: float  # (m/s)
    距地面50m处北向风速: float  # (m/s)


class 设备:
    def __init__(
        self,
        model:ConcreteModel,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表:list = [],
        输入类型列表:list = [],
    ):
        self.model = model
        self.生产厂商 = 生产厂商
        self.生产型号 = 生产型号
        self.设备额定运行参数 = 设备额定运行参数
        self.设备运行约束 = 设备运行约束
        self.设备经济性参数 = 设备经济性参数
        self.设备工况 = 设备工况

        self.环境 = environ

        self.设备配置台数 = 设备配置台数 if 设备配置台数 is not None else Var(domain=NonNegativeIntegers)
        
        self.输入功率 = {}
        self.输出功率 = {}
        self.建立输入功率(输入类型列表)
        self.建立输出功率(输出类型列表)

    def 建立输入功率(self,input_types):
        for input_type in input_types:
            self.输入功率[input_type] = VarList()

    def 建立输出功率(self,output_types):
        for output_type in output_types:
            self.输出功率[output_type] = VarList()


class 光伏(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=['电'], # add this later.
            输入类型列表=[]
        )
        ## 设置设备额定运行参数 ##
        self.单个光伏板面积 = self.设备额定运行参数["单个光伏板面积"]
        """单位：(m²)"""
        self.光电转换效率 = self.设备额定运行参数["光电转换效率"]
        """单位：(%)"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """0<x<1"""
        
        ## 设置设备运行约束 ##
        self.最大发电功率 = self.设备运行约束['最大发电功率']
        """单位：(kW)"""

        ## 设备经济性参数 ##
        self.采购成本 = self.设备经济性参数['采购成本']  
        """单位：(万元/台)"""
        self.固定维护成本 = self.设备经济性参数['固定维护成本']  
        """单位：(万元/年)"""
        self.可变维护成本 = self.设备经济性参数['可变维护成本']  
        """单位：(元/kWh)"""
        self.设计寿命 = self.设备经济性参数['设计寿命']  
        """单位：(年)"""

    def add_constraints(
        self):
        光照强度 = self.环境.太阳辐射强度
        self.model
        Constraint(self.输出功率['电'] <= self.设备配置台数 * self.光电转换效率 * 光照强度 * self.单个光伏板面积*self.功率因数
        self.输出功率['电'] <= self.最大发电功率*self.功率因数
        ###错的

    def 设备运行约束(self):
        self.model.add_constraint(self.输出功率 <= self.最大输出功率)

    def 设备经济性参数(self, model, 采购成本: float, 固定维护成本: float, 可变维护成本: float, 设计寿命: float):
        self.采购成本 = 采购成本  # (万元/台)
        self.固定维护成本 = 固定维护成本  # (万元/年)
        self.可变维护成本 = 可变维护成本  # (元/kWh)
        self.设计寿命 = 设计寿命  # (年)

    def 设备经济约束(self):
        self.成本 = (
            self.可变维护成本 * self.输出功率 + self.固定维护成本 * self.设计寿命 + self.采购成本 * self.设备数量
        )
