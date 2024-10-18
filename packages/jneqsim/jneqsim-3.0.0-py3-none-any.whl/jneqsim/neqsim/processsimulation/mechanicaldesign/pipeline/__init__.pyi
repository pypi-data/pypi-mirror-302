
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.neqsim.processsimulation.mechanicaldesign
import jneqsim.neqsim.processsimulation.processequipment
import typing



class PipelineMechanicalDesign(jneqsim.neqsim.processsimulation.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.neqsim.processsimulation.processequipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...
    def readDesignSpecifications(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processsimulation.mechanicaldesign.pipeline")``.

    PipelineMechanicalDesign: typing.Type[PipelineMechanicalDesign]
