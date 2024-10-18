
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class Conductivity(jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.ConductivityInterface):
    pureComponentConductivity: typing.MutableSequence[float] = ...
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcConductivity(self) -> float: ...
    def calcPureComponentConductivity(self) -> None: ...
    def clone(self) -> 'Conductivity': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.conductivity")``.

    Conductivity: typing.Type[Conductivity]
