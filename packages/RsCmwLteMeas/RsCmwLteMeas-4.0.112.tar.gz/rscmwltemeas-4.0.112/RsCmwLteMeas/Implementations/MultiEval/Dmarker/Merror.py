from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MerrorCls:
	"""Merror commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("merror", core, parent)

	def fetch(self, xvalue: int or bool, trace_select: enums.TraceSelect, deltaMarker=repcap.DeltaMarker.Default) -> float:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:DMARker<No>:MERRor \n
		Snippet: value: float = driver.multiEval.dmarker.merror.fetch(xvalue = 1, trace_select = enums.TraceSelect.AVERage, deltaMarker = repcap.DeltaMarker.Default) \n
		Uses the markers 1 and 2 with relative values on the bar graphs: EVM RMS, EVM peak, magnitude error and phase error vs
		SC-FDMA symbol. \n
		Use RsCmwLteMeas.reliability.last_value to read the updated reliability indicator. \n
			:param xvalue: (integer or boolean) integer X value of the marker position relative to the X value of the reference marker There are two X values per SC-FDMA symbol on the X axis (symbol 0 low, symbol 0 high, ..., symbol 6 low, symbol 6 high) . Range: -13 to 13
			:param trace_select: CURRent | AVERage | MAXimum
			:param deltaMarker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dmarker')
			:return: yvalue: float Y value of the marker position relative to the Y value of the reference marker"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('xvalue', xvalue, DataType.IntegerExt), ArgSingle('trace_select', trace_select, DataType.Enum, enums.TraceSelect))
		deltaMarker_cmd_val = self._cmd_group.get_repcap_cmd_value(deltaMarker, repcap.DeltaMarker)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:LTE:MEASurement<Instance>:MEValuation:DMARker{deltaMarker_cmd_val}:MERRor? {param}'.rstrip(), suppressed)
		return Conversions.str_to_float(response)
