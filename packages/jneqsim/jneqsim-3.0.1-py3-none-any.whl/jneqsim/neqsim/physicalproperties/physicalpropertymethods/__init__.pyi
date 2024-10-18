
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.solidphysicalproperties
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class PhysicalPropertyMethodInterface(java.lang.Cloneable, java.io.Serializable):
    def clone(self) -> 'PhysicalPropertyMethodInterface': ...
    def setPhase(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface) -> None: ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...

class PhysicalPropertyMethod(PhysicalPropertyMethodInterface):
    def __init__(self): ...
    def clone(self) -> 'PhysicalPropertyMethod': ...
    def setPhase(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface) -> None: ...
    def tuneModel(self, double: float, double2: float, double3: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods")``.

    PhysicalPropertyMethod: typing.Type[PhysicalPropertyMethod]
    PhysicalPropertyMethodInterface: typing.Type[PhysicalPropertyMethodInterface]
    commonphasephysicalproperties: jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.__module_protocol__
    gasphysicalproperties: jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.__module_protocol__
    liquidphysicalproperties: jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.__module_protocol__
    methodinterface: jneqsim.neqsim.physicalproperties.physicalpropertymethods.methodinterface.__module_protocol__
    solidphysicalproperties: jneqsim.neqsim.physicalproperties.physicalpropertymethods.solidphysicalproperties.__module_protocol__
