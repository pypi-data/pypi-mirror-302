"""
delta-complete SMT solver for linear theories over the reals
"""
from __future__ import annotations
from pydlinear._pydlinear import BoundPropagationType
from pydlinear._pydlinear import Box
from pydlinear._pydlinear import Config
from pydlinear._pydlinear import Expression
from pydlinear._pydlinear import Format
from pydlinear._pydlinear import Formula
from pydlinear._pydlinear import Interval
from pydlinear._pydlinear import LPMode
from pydlinear._pydlinear import LPSolver
from pydlinear._pydlinear import PreprocessingRunningFrequency
from pydlinear._pydlinear import SatDefaultPhase
from pydlinear._pydlinear import SatSolver
from pydlinear._pydlinear import SmtResult
from pydlinear._pydlinear import SmtSolver
from pydlinear._pydlinear import SmtSolverOutput
from pydlinear._pydlinear import Variable
from pydlinear._pydlinear import VariableType
from pydlinear._pydlinear import Variables
from pydlinear._pydlinear import set_verbosity
from . import _pydlinear
__all__ = ['BoundPropagationType', 'Box', 'Config', 'Expression', 'Format', 'Formula', 'Interval', 'LOG_CRITICAL', 'LOG_DEBUG', 'LOG_ERROR', 'LOG_INFO', 'LOG_NONE', 'LOG_TRACE', 'LOG_WARN', 'LPMode', 'LPSolver', 'PreprocessingRunningFrequency', 'SatDefaultPhase', 'SatSolver', 'SmtResult', 'SmtSolver', 'SmtSolverOutput', 'Variable', 'VariableType', 'Variables', 'set_verbosity']
LOG_CRITICAL: int = 0
LOG_DEBUG: int = 4
LOG_ERROR: int = 1
LOG_INFO: int = 3
LOG_NONE: int = -1
LOG_TRACE: int = 5
LOG_WARN: int = 2
__pydlinear_doc__: str = 'delta-complete SMT solver for linear theories over the reals'
__pydlinear_version__: str = '0.0.1'
__version__: str = '0.0.1'
