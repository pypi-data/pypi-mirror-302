
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertymethods
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.conductivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.density
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.diffusivity
import jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.viscosity
import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import typing



class GasPhysicalPropertyMethod(jneqsim.neqsim.physicalproperties.physicalpropertymethods.PhysicalPropertyMethod):
    binaryMolecularDiameter: typing.MutableSequence[typing.MutableSequence[float]] = ...
    binaryEnergyParameter: typing.MutableSequence[typing.MutableSequence[float]] = ...
    binaryMolecularMass: typing.MutableSequence[typing.MutableSequence[float]] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface): ...
    def setPhase(self, physicalPropertiesInterface: jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalPropertiesInterface) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties")``.

    GasPhysicalPropertyMethod: typing.Type[GasPhysicalPropertyMethod]
    conductivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.conductivity.__module_protocol__
    density: jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.density.__module_protocol__
    diffusivity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.diffusivity.__module_protocol__
    viscosity: jneqsim.neqsim.physicalproperties.physicalpropertymethods.gasphysicalproperties.viscosity.__module_protocol__
