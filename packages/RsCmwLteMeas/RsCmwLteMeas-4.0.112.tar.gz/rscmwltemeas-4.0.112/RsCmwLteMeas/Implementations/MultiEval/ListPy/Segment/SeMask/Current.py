from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment
			- Statist_Expired: int: decimal Reached statistical length in slots
			- Out_Of_Tolerance: int: decimal Percentage of measured subframes with failed limit check Unit: %
			- Obw: float: float Occupied bandwidth Unit: Hz
			- Tx_Power: float: float Total TX power in the slot Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Obw'),
			ArgStruct.scalar_float('Tx_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Obw: float = None
			self.Tx_Power: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SEMask:CURRent \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.seMask.current.fetch(segment = repcap.Segment.Default) \n
		Return spectrum emission single value results for segment <no> in list mode. The values described below are returned by
		FETCh commands. The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands.
		The remaining values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SEMask:CURRent?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment
			- Statist_Expired: int: decimal Reached statistical length in slots
			- Out_Of_Tolerance: int: decimal Percentage of measured subframes with failed limit check Unit: %
			- Obw: float or bool: float Occupied bandwidth Unit: Hz
			- Tx_Power: float or bool: float Total TX power in the slot Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float_ext('Obw'),
			ArgStruct.scalar_float_ext('Tx_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Obw: float or bool = None
			self.Tx_Power: float or bool = None

	def calculate(self, segment=repcap.Segment.Default) -> CalculateStruct:
		"""SCPI: CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SEMask:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.listPy.segment.seMask.current.calculate(segment = repcap.Segment.Default) \n
		Return spectrum emission single value results for segment <no> in list mode. The values described below are returned by
		FETCh commands. The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands.
		The remaining values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CALCulate:LTE:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SEMask:CURRent?', self.__class__.CalculateStruct())
