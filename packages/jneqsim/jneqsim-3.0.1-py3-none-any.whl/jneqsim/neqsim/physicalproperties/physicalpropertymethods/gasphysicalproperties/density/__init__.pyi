
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class Density(jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.GasPhysicalPropertyMethod, jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.DensityInterface):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcDensity(self) -> float: ...
    def clone(self) -> 'Density': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.density")``.

    Density: typing.Type[Density]
