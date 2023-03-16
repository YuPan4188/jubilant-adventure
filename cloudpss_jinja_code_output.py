# from pydantic import BaseModel
# is the BaseModel needed?
from pyomo.environ import *
from dataclasses import dataclass
import uuid

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


import datetime


@dataclass
class 模拟参数:
    开始时间: datetime.datetime
    结束时间: datetime.datetime
    步长: float  # 单位：分钟

    @property
    def 仿真时长(self):
        """
        返回单位: 天
        """
        return (self.结束时间 - self.开始时间).days  # int


@dataclass
class 设备:
    def __init__(
        self,
        model: ConcreteModel,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        self.model = model
        self.uuid = str(uuid.uuid4())
        self.生产厂商 = 生产厂商
        self.生产型号 = 生产型号
        self.设备额定运行参数 = 设备额定运行参数
        self.设备运行约束 = 设备运行约束
        self.设备经济性参数 = 设备经济性参数
        self.设备工况 = 设备工况

        self.环境 = environ
        self.模拟参数 = simulation_params

        self.设备配置台数 = 设备配置台数 if 设备配置台数 is not None else Var(domain=NonNegativeIntegers)

        self.输入功率 = {}
        self.输出功率 = {}
        self.输入类型列表 = 输入类型列表
        self.输出类型列表 = 输出类型列表
        self.建立输入功率(输入类型列表)
        self.建立输出功率(输出类型列表)

    def 建立输入功率(self, input_types):
        for input_type in input_types:
            self.输入功率[input_type] = VarList()
            self.model.add_component(
                f"{self.uuid}_输入功率_{input_type}", self.输入功率[input_type]
            )

    def 建立输出功率(self, output_types):
        for output_type in output_types:
            self.输出功率[output_type] = VarList()
            self.model.add_component(
                f"{self.uuid}_输出功率_{output_type}", self.输出功率[output_type]
            )class 光伏(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.单个光伏板面积 = self.设备额定运行参数["单个光伏板面积"]  * 1e-06
        """单位：(kilometer ** 2) <- (meter ** 2) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.最大发电功率 = self.设备运行约束["最大发电功率"] 
        """单位：(kilowatt) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 风机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定容量 = self.设备额定运行参数["额定容量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.塔筒高度 = self.设备额定运行参数["塔筒高度"]  * 0.001
        """单位：(kilometer) <- (meter) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气轮机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定发电功率 = self.设备额定运行参数["额定发电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气内燃机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定发电功率 = self.设备额定运行参数["额定发电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蒸汽轮机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大发电量 = self.设备运行约束["最大发电量"] 
        """单位：(kilowatt) 设备运行约束"""
        self.最小发电量 = self.设备运行约束["最小发电量"] 
        """单位：(kilowatt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热泵(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定制热量 = self.设备额定运行参数["额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气热水锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气蒸汽锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热热水锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热蒸汽锅炉-单压(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热蒸汽锅炉-双压(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热管式太阳能集热器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.单个集热器面积 = self.设备额定运行参数["单个集热器面积"]  * 1e-06
        """单位：(kilometer ** 2) <- (meter ** 2) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 电压缩制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定制冷量 = self.设备额定运行参数["额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热水吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 烟气吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蒸汽吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"] 
        """单位：(volt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄冰空调(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定放冷功率 = self.设备额定运行参数["额定放冷功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.额定蓄冷功率 = self.设备额定运行参数["额定蓄冷功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.蓄冰空调最大容量 = self.设备运行约束["蓄冰空调最大容量"] 
        """单位：(kilowatt_hour) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄热电锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定放热功率 = self.设备额定运行参数["额定放热功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.额定蓄热功率 = self.设备额定运行参数["额定蓄热功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.蓄热电锅炉最大容量 = self.设备运行约束["蓄热电锅炉最大容量"] 
        """单位：(kilowatt_hour) 设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄电池(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定充电功率 = self.设备额定运行参数["额定充电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.额定放电功率 = self.设备额定运行参数["额定放电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.电池最大容量 = self.设备运行约束["电池最大容量"] 
        """单位：(kilowatt_hour) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 变压器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.副边侧额定电压有效值 = self.设备额定运行参数["副边侧额定电压有效值"] 
        """单位：(volt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.原边侧额定电压有效值 = self.设备额定运行参数["原边侧额定电压有效值"]  * 1000.0
        """单位：(volt) <- (kilovolt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定容量 = self.设备额定运行参数["额定容量"]  * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 传输线(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定电压 = self.设备额定运行参数["额定电压"]  * 1000.0
        """单位：(volt) <- (kilovolt) 设备额定运行参数"""
        self.额定频率 = self.设备额定运行参数["额定频率"] 
        """单位：(hertz) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 电容器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定容量 = self.设备额定运行参数["额定容量"]  * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) 设备额定运行参数"""
        self.额定电压有效值 = self.设备额定运行参数["额定电压有效值"] 
        """单位：(hertz) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 离心泵(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.最低进口压力 = self.设备运行约束["最低进口压力"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        self.最大进口压力 = self.设备运行约束["最大进口压力"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 换热器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定热负荷 = self.设备额定运行参数["额定热负荷"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 管道(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.管道内径 = self.设备额定运行参数["管道内径"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        self.管道壁厚 = self.设备额定运行参数["管道壁厚"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.管道粗糙度 = self.设备额定运行参数["管道粗糙度"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.管道设计压力 = self.设备运行约束["管道设计压力"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.[] = self.设备经济性参数["[]"] 
        """设备经济性参数"""
        self.设计寿命 = self.设备经济性参数["设计寿命"] 
        """单位：(年) 设备经济性参数"""
        
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 光伏_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.光伏板面积 = self.设备额定运行参数["光伏板面积"]  * 1e-06
        """单位：(kilometer ** 2) <- (meter ** 2) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.最大发电功功率 = self.设备运行约束["最大发电功功率"] 
        """单位：(kilowatt) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 风机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定发电量 = self.设备额定运行参数["额定发电量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.轮毂高度 = self.设备额定运行参数["轮毂高度"]  * 0.001
        """单位：(kilometer) <- (meter) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气轮机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气内燃机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定发电功率 = self.设备额定运行参数["额定发电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蒸汽轮机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.[] = self.设备运行约束["[]"] 
        """设备运行约束"""
        self.最大发电量 = self.设备运行约束["最大发电量"] 
        """单位：(kilowatt) 设备运行约束"""
        self.最小发电量 = self.设备运行约束["最小发电量"] 
        """单位：(kilowatt) 设备运行约束"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]  * 1000000000.0
        """单位：(millipascal) <- (megapascal) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热泵_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定制热量 = self.设备额定运行参数["额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气热水锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 燃气蒸汽锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热热水锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热蒸汽锅炉-单压_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 余热蒸汽锅炉-双压_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热管式太阳能集热器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.集热器面积 = self.设备额定运行参数["集热器面积"]  * 1e-06
        """单位：(kilometer ** 2) <- (meter ** 2) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 电压缩制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定制冷量 = self.设备额定运行参数["额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 热水吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 烟气吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蒸汽吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.用电功率 = self.设备额定运行参数["用电功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄冰空调_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定放冷功率 = self.设备额定运行参数["额定放冷功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.额定蓄冷功率 = self.设备额定运行参数["额定蓄冷功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄热电锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定放热功率 = self.设备额定运行参数["额定放热功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.额定蓄热功率 = self.设备额定运行参数["额定蓄热功率"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 蓄电池_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##self.电池最大容量 = self.设备运行约束["电池最大容量"] 
        """单位：(kilowatt_hour) 设备运行约束"""
        self.最大充电功率 = self.设备运行约束["最大充电功率"] 
        """单位：(kilowatt) 设备运行约束"""
        self.最大放电功率 = self.设备运行约束["最大放电功率"] 
        """单位：(kilowatt) 设备运行约束"""
        
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 储水罐_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.罐底面积 = self.设备额定运行参数["罐底面积"]  * 1e-06
        """单位：(kilometer ** 2) <- (meter ** 2) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 变压器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.一次侧短路电抗 = self.设备额定运行参数["一次侧短路电抗"] 
        """单位：(ohm) 设备额定运行参数"""
        self.一次侧短路电阻 = self.设备额定运行参数["一次侧短路电阻"] 
        """单位：(ohm) 设备额定运行参数"""
        self.额定容量 = self.设备额定运行参数["额定容量"]  * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 传输线_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 电容器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定容量 = self.设备额定运行参数["额定容量"]  * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) 设备额定运行参数"""
        self.额定电压有效值 = self.设备额定运行参数["额定电压有效值"] 
        """单位：(hertz) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 模块化多电平变流器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.额定电压 = self.设备额定运行参数["额定电压"]  * 1000.0
        """单位：(volt) <- (kilovolt) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 离心泵_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 换热器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.额定热负荷 = self.设备额定运行参数["额定热负荷"] 
        """单位：(kilowatt) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
class 管道_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##self.管道内径 = self.设备额定运行参数["管道内径"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        self.管道壁厚 = self.设备额定运行参数["管道壁厚"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        self.[] = self.设备额定运行参数["[]"] 
        """设备额定运行参数"""
        self.管道粗糙度 = self.设备额定运行参数["管道粗糙度"]  * 1e-06
        """单位：(kilometer) <- (millimeter) 设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        ## 设置设备经济性参数 ##
        
        ## 设置设备工况 ##
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...
