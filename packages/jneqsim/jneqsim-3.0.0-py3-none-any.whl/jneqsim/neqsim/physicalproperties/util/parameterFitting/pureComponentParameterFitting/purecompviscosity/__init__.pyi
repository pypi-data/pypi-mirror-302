
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.physicalproperties.util.parameterFitting.pureComponentParameterFitting.purecompviscosity.chungMethod
import jneqsim.neqsim.physicalproperties.util.parameterFitting.pureComponentParameterFitting.purecompviscosity.linearLiquidModel
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.physicalproperties.util.parameterFitting.pureComponentParameterFitting.purecompviscosity")``.

    chungMethod: jneqsim.neqsim.physicalproperties.util.parameterFitting.pureComponentParameterFitting.purecompviscosity.chungMethod.__module_protocol__
    linearLiquidModel: jneqsim.neqsim.physicalproperties.util.parameterFitting.pureComponentParameterFitting.purecompviscosity.linearLiquidModel.__module_protocol__
