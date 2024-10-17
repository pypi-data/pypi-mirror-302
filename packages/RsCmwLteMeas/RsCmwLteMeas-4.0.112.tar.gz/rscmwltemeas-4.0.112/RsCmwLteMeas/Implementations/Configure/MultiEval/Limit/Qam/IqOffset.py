from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqOffsetCls:
	"""IqOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqOffset", core, parent)

	def set(self, enable: bool, offset_1: float, offset_2: float, offset_3: float, qAMmodOrder=repcap.QAMmodOrder.Default) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:QAM<ModOrder>:IQOFfset \n
		Snippet: driver.configure.multiEval.limit.qam.iqOffset.set(enable = False, offset_1 = 1.0, offset_2 = 1.0, offset_3 = 1.0, qAMmodOrder = repcap.QAMmodOrder.Default) \n
		Defines upper limits for the I/Q origin offset, for QAM modulations. Three different I/Q origin offset limits can be set
		for three TX power ranges. For details, see 'I/Q origin offset limits'. \n
			:param enable: OFF | ON OFF: disables the limit check ON: enables the limit check
			:param offset_1: numeric I/Q origin offset limit for high TX power range Range: -256 dBc to 256 dBc, Unit: dBc
			:param offset_2: numeric I/Q origin offset limit for intermediate TX power range Range: -256 dBc to 256 dBc, Unit: dBc
			:param offset_3: numeric I/Q origin offset limit for low TX power range Range: -256 dBc to 256 dBc, Unit: dBc
			:param qAMmodOrder: optional repeated capability selector. Default value: Qam16 (settable in the interface 'Qam')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('offset_1', offset_1, DataType.Float), ArgSingle('offset_2', offset_2, DataType.Float), ArgSingle('offset_3', offset_3, DataType.Float))
		qAMmodOrder_cmd_val = self._cmd_group.get_repcap_cmd_value(qAMmodOrder, repcap.QAMmodOrder)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:QAM{qAMmodOrder_cmd_val}:IQOFfset {param}'.rstrip())

	# noinspection PyTypeChecker
	class IqOffsetStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the limit check ON: enables the limit check
			- Offset_1: float: numeric I/Q origin offset limit for high TX power range Range: -256 dBc to 256 dBc, Unit: dBc
			- Offset_2: float: numeric I/Q origin offset limit for intermediate TX power range Range: -256 dBc to 256 dBc, Unit: dBc
			- Offset_3: float: numeric I/Q origin offset limit for low TX power range Range: -256 dBc to 256 dBc, Unit: dBc"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Offset_1'),
			ArgStruct.scalar_float('Offset_2'),
			ArgStruct.scalar_float('Offset_3')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Offset_1: float = None
			self.Offset_2: float = None
			self.Offset_3: float = None

	def get(self, qAMmodOrder=repcap.QAMmodOrder.Default) -> IqOffsetStruct:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:QAM<ModOrder>:IQOFfset \n
		Snippet: value: IqOffsetStruct = driver.configure.multiEval.limit.qam.iqOffset.get(qAMmodOrder = repcap.QAMmodOrder.Default) \n
		Defines upper limits for the I/Q origin offset, for QAM modulations. Three different I/Q origin offset limits can be set
		for three TX power ranges. For details, see 'I/Q origin offset limits'. \n
			:param qAMmodOrder: optional repeated capability selector. Default value: Qam16 (settable in the interface 'Qam')
			:return: structure: for return value, see the help for IqOffsetStruct structure arguments."""
		qAMmodOrder_cmd_val = self._cmd_group.get_repcap_cmd_value(qAMmodOrder, repcap.QAMmodOrder)
		return self._core.io.query_struct(f'CONFigure:LTE:MEASurement<Instance>:MEValuation:LIMit:QAM{qAMmodOrder_cmd_val}:IQOFfset?', self.__class__.IqOffsetStruct())
