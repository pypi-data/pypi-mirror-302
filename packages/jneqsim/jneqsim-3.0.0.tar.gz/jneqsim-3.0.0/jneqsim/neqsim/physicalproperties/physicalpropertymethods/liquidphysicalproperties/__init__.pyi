
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.conductivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.density
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.diffusivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.viscosity
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class LiquidPhysicalPropertyMethod(jneqsim.neqsim.physicalproperties.physicalpropertymethods.PhysicalPropertyMethod):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def setPhase(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties")``.

    LiquidPhysicalPropertyMethod: typing.Type[LiquidPhysicalPropertyMethod]
    conductivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.conductivity.__module_protocol__
    density: jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.density.__module_protocol__
    diffusivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.diffusivity.__module_protocol__
    viscosity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.liquidphysicalproperties.viscosity.__module_protocol__
