
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import jneqsim.neqsim.processsimulation.costestimation.compressor
import jneqsim.neqsim.processsimulation.costestimation.separator
import jneqsim.neqsim.processsimulation.costestimation.valve
import jneqsim.neqsim.processsimulation.mechanicaldesign
import typing



class CostEstimateBaseClass(java.io.Serializable):
    @typing.overload
    def __init__(self, systemMechanicalDesign: jneqsim.neqsim.processsimulation.mechanicaldesign.SystemMechanicalDesign): ...
    @typing.overload
    def __init__(self, systemMechanicalDesign: jneqsim.neqsim.processsimulation.mechanicaldesign.SystemMechanicalDesign, double: float): ...
    def equals(self, object: typing.Any) -> bool: ...
    def getCAPEXestimate(self) -> float: ...
    def getWeightBasedCAPEXEstimate(self) -> float: ...
    def hashCode(self) -> int: ...

class UnitCostEstimateBaseClass(java.io.Serializable):
    mechanicalEquipment: jneqsim.neqsim.processsimulation.mechanicaldesign.MechanicalDesign = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, mechanicalDesign: jneqsim.neqsim.processsimulation.mechanicaldesign.MechanicalDesign): ...
    def equals(self, object: typing.Any) -> bool: ...
    def getTotaltCost(self) -> float: ...
    def hashCode(self) -> int: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processsimulation.costestimation")``.

    CostEstimateBaseClass: typing.Type[CostEstimateBaseClass]
    UnitCostEstimateBaseClass: typing.Type[UnitCostEstimateBaseClass]
    compressor: jneqsim.neqsim.processsimulation.costestimation.compressor.__module_protocol__
    separator: jneqsim.neqsim.processsimulation.costestimation.separator.__module_protocol__
    valve: jneqsim.neqsim.processsimulation.costestimation.valve.__module_protocol__
