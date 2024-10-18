
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class Diffusivity(jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.GasPhysicalPropertyMethod, jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.DiffusivityInterface):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcBinaryDiffusionCoefficient(self, int: int, int2: int, int3: int) -> float: ...
    def calcDiffusionCoefficients(self, int: int, int2: int) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def calcEffectiveDiffusionCoefficients(self) -> None: ...
    def clone(self) -> 'Diffusivity': ...
    def getEffectiveDiffusionCoefficient(self, int: int) -> float: ...
    def getFickBinaryDiffusionCoefficient(self, int: int, int2: int) -> float: ...
    def getMaxwellStefanBinaryDiffusionCoefficient(self, int: int, int2: int) -> float: ...

class WilkeLeeDiffusivity(Diffusivity):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcBinaryDiffusionCoefficient(self, int: int, int2: int, int3: int) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.diffusivity")``.

    Diffusivity: typing.Type[Diffusivity]
    WilkeLeeDiffusivity: typing.Type[WilkeLeeDiffusivity]
