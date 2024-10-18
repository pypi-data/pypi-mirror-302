
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.processsimulation.costestimation
import jneqsim.neqsim.processsimulation.mechanicaldesign.valve
import typing



class ValveCostEstimate(jneqsim.neqsim.processsimulation.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, valveMechanicalDesign: jneqsim.neqsim.processsimulation.mechanicaldesign.valve.ValveMechanicalDesign): ...
    def getTotaltCost(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processsimulation.costestimation.valve")``.

    ValveCostEstimate: typing.Type[ValveCostEstimate]
