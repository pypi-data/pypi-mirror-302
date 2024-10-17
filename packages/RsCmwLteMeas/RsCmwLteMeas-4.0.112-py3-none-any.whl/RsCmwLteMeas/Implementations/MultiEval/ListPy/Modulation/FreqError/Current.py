from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:FERRor:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.freqError.current.fetch() \n
		Return carrier frequency error values for all measured list mode segments. The values described below are returned by
		FETCh commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency_error: float Comma-separated list of values, one per measured segment Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:FERRor:CURRent?', suppressed)
		return response

	def calculate(self) -> List[float or bool]:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:FERRor:CURRent \n
		Snippet: value: List[float or bool] = driver.multiEval.listPy.modulation.freqError.current.calculate() \n
		Return carrier frequency error values for all measured list mode segments. The values described below are returned by
		FETCh commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency_error: (float or boolean items) float Comma-separated list of values, one per measured segment Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:MODulation:FERRor:CURRent?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
