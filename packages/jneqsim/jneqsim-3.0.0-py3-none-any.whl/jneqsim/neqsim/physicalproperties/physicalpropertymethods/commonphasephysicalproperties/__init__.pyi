
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.conductivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.diffusivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.viscosity
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class CommonPhysicalPropertyMethod(jneqsim.neqsim.physicalproperties.physicalpropertymethods.PhysicalPropertyMethod):
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def setPhase(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties")``.

    CommonPhysicalPropertyMethod: typing.Type[CommonPhysicalPropertyMethod]
    conductivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.conductivity.__module_protocol__
    diffusivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.diffusivity.__module_protocol__
    viscosity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.commonphasephysicalproperties.viscosity.__module_protocol__
