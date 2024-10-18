
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.physicalpropertysystem
import jneqsim.neqsim.thermo.phase
import typing



class SolidPhysicalProperties(jneqsim.neqsim.physicalproperties.physicalpropertysystem.PhysicalProperties):
    def __init__(self, phaseInterface: jneqsim.neqsim.thermo.phase.PhaseInterface): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.physicalpropertysystem.solidphysicalproperties")``.

    SolidPhysicalProperties: typing.Type[SolidPhysicalProperties]
