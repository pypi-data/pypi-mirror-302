
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import neqsim
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class ChungViscosityMethod(jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.viscosity.Viscosity):
    pureComponentViscosity: typing.MutableSequence[float] = ...
    relativeViscosity: typing.MutableSequence[float] = ...
    Fc: typing.MutableSequence[float] = ...
    omegaVisc: typing.MutableSequence[float] = ...
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcViscosity(self) -> float: ...
    def getPureComponentViscosity(self, int: int) -> float: ...
    def initChungPureComponentViscosity(self) -> None: ...

class Viscosity: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.viscosity")``.

    ChungViscosityMethod: typing.Type[ChungViscosityMethod]
    Viscosity: typing.Type[Viscosity]
