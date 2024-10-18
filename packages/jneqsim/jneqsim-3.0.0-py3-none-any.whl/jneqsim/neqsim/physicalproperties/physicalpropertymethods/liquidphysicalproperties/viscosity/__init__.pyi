
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class Viscosity(jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.LiquidPhysicalPropertyMethod, jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.ViscosityInterface):
    pureComponentViscosity: typing.MutableSequence[float] = ...
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcPureComponentViscosity(self) -> None: ...
    def calcViscosity(self) -> float: ...
    def clone(self) -> 'Viscosity': ...
    def getPureComponentViscosity(self, int: int) -> float: ...
    def getViscosityPressureCorrection(self, int: int) -> float: ...

class AmineViscosity(Viscosity):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcViscosity(self) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.viscosity")``.

    AmineViscosity: typing.Type[AmineViscosity]
    Viscosity: typing.Type[Viscosity]
