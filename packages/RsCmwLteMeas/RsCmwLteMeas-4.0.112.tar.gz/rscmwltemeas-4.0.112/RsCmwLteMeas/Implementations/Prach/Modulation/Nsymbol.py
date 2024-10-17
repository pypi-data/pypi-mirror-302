from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsymbolCls:
	"""Nsymbol commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nsymbol", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:PRACh:MODulation:NSYMbol \n
		Snippet: value: int = driver.prach.modulation.nsymbol.fetch() \n
		Queries the number of active OFDM symbols (symbols with result bars) in the EVM vs symbol bar graph. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: no_of_symbols: decimal"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:PRACh:MODulation:NSYMbol?', suppressed)
		return Conversions.str_to_int(response)
