
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.processsimulation.costestimation
import jneqsim.neqsim.processsimulation.mechanicaldesign.compressor
import typing



class CompressorCostEstimate(jneqsim.neqsim.processsimulation.costestimation.UnitCostEstimateBaseClass):
    def __init__(self, compressorMechanicalDesign: jneqsim.neqsim.processsimulation.mechanicaldesign.compressor.CompressorMechanicalDesign): ...
    def getTotaltCost(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processsimulation.costestimation.compressor")``.

    CompressorCostEstimate: typing.Type[CompressorCostEstimate]
