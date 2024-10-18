
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.processsimulation.util.monitor
import jneqsim.neqsim.processsimulation.util.report
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processsimulation.util")``.

    monitor: jneqsim.neqsim.processsimulation.util.monitor.__module_protocol__
    report: jneqsim.neqsim.processsimulation.util.report.__module_protocol__
