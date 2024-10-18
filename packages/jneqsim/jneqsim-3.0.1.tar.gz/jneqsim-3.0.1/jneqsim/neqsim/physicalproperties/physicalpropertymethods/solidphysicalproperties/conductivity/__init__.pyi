
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.solidphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class Conductivity(jneqsim.neqsim.physicalproperties.physicalpropertymethods.solidphysicalproperties.SolidPhysicalPropertyMethod, jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.ConductivityInterface):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def calcConductivity(self) -> float: ...
    def clone(self) -> 'Conductivity': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.solidphysicalproperties.conductivity")``.

    Conductivity: typing.Type[Conductivity]
