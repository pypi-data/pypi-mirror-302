from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Utra_2_Neg: float: float Power in the second UTRA channel with lower frequency Unit: dBm
			- Utra_1_Neg: float: float Power in the first UTRA channel with lower frequency Unit: dBm
			- Eutra_Negativ: float: float Power in the first E-UTRA channel with lower frequency Unit: dBm
			- Eutra: float: float Power in the allocated E-UTRA channel Unit: dBm
			- Eutra_Positiv: float: float Power in the first E-UTRA channel with higher frequency Unit: dBm
			- Utra_1_Pos: float: float Power in the first UTRA channel with higher frequency Unit: dBm
			- Utra_2_Pos: float: float Power in the second UTRA channel with higher frequency Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Utra_2_Neg'),
			ArgStruct.scalar_float('Utra_1_Neg'),
			ArgStruct.scalar_float('Eutra_Negativ'),
			ArgStruct.scalar_float('Eutra'),
			ArgStruct.scalar_float('Eutra_Positiv'),
			ArgStruct.scalar_float('Utra_1_Pos'),
			ArgStruct.scalar_float('Utra_2_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: float = None
			self.Utra_1_Neg: float = None
			self.Eutra_Negativ: float = None
			self.Eutra: float = None
			self.Eutra_Positiv: float = None
			self.Utra_1_Pos: float = None
			self.Utra_2_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage \n
		Snippet: value: ResultData = driver.multiEval.trace.aclr.average.read() \n
		Returns the absolute powers as displayed in the ACLR diagram. The current and average values can be retrieved. See also
		'View Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage \n
		Snippet: value: ResultData = driver.multiEval.trace.aclr.average.fetch() \n
		Returns the absolute powers as displayed in the ACLR diagram. The current and average values can be retrieved. See also
		'View Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:LTE:MEASurement<Instance>:MEValuation:TRACe:ACLR:AVERage?', self.__class__.ResultData())
