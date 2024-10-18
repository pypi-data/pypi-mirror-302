
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jneqsim.neqsim.physicalproperties.interfaceproperties
import jneqsim.neqsim.physicalproperties.mixingrule
import jneqsim.neqsim.physicalproperties.physicalpropertymethods
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import jneqsim.neqsim.physicalproperties.util
import jneqsim.neqsim.thermo.phase
import typing



class PhysicalPropertyHandler(java.lang.Cloneable, java.io.Serializable):
    def __init__(self): ...
    def clone(self) -> 'PhysicalPropertyHandler': ...
    def getPhysicalProperty(self, phaseInterface: jneqsim.neqsim.thermo.phase.PhaseInterface) -> jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface: ...
    def setPhysicalProperties(self, phaseInterface: jneqsim.neqsim.thermo.phase.PhaseInterface, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties")``.

    PhysicalPropertyHandler: typing.Type[PhysicalPropertyHandler]
    interfaceproperties: jneqsim.neqsim.physicalproperties.interfaceproperties.__module_protocol__
    mixingrule: jneqsim.neqsim.physicalproperties.mixingrule.__module_protocol__
    physicalpropertymethods: jneqsim.neqsim.physicalproperties.physicalpropertymethods.__module_protocol__
    physicalpropertysystem: jneqsim.neqsim.physicalproperties.physicalpropertysystem.__module_protocol__
    util: jneqsim.neqsim.physicalproperties.util.__module_protocol__
