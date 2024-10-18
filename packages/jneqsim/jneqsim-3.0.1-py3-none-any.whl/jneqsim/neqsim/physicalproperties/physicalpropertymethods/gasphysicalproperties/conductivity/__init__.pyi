
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class ChungConductivityMethod(jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.conductivity.Conductivity):
    pureComponentConductivity: typing.MutableSequence[float] = ...
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcConductivity(self) -> float: ...
    def calcPureComponentConductivity(self) -> None: ...

class Conductivity: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.conductivity")``.

    ChungConductivityMethod: typing.Type[ChungConductivityMethod]
    Conductivity: typing.Type[Conductivity]
