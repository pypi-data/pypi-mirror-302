from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModulationCls:
	"""Modulation commands group definition. 7 total commands, 2 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulation", core, parent)

	@property
	def sindex(self):
		"""sindex commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sindex'):
			from .Sindex import SindexCls
			self._sindex = SindexCls(self._core, self._cmd_group)
		return self._sindex

	@property
	def ewLength(self):
		"""ewLength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ewLength'):
			from .EwLength import EwLengthCls
			self._ewLength = EwLengthCls(self._core, self._cmd_group)
		return self._ewLength

	def get_lrs_index(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:LRSindex \n
		Snippet: value: int = driver.configure.prach.modulation.get_lrs_index() \n
		Specifies the logical root sequence index to be used for generation of the preamble sequence. For the combined signal
		path scenario, use CONFigure:LTE:SIGN<i>:CELL:PRACh:LRSindex. \n
			:return: log_root_seq_index: numeric Range: 0 to 837 (for preamble format 4: 0 to 137)
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:LRSindex?')
		return Conversions.str_to_int(response)

	def set_lrs_index(self, log_root_seq_index: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:LRSindex \n
		Snippet: driver.configure.prach.modulation.set_lrs_index(log_root_seq_index = 1) \n
		Specifies the logical root sequence index to be used for generation of the preamble sequence. For the combined signal
		path scenario, use CONFigure:LTE:SIGN<i>:CELL:PRACh:LRSindex. \n
			:param log_root_seq_index: numeric Range: 0 to 837 (for preamble format 4: 0 to 137)
		"""
		param = Conversions.decimal_value_to_str(log_root_seq_index)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:LRSindex {param}')

	def get_zcz_config(self) -> int:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:ZCZConfig \n
		Snippet: value: int = driver.configure.prach.modulation.get_zcz_config() \n
		Specifies the zero correlation zone config, i.e. which NCS value of an NCS set is used for generation of the preamble
		sequence. For the combined signal path scenario, use CONFigure:LTE:SIGN<i>:CELL:PRACh:ZCZConfig. \n
			:return: zero_corr_zone_con: numeric Range: 0 to 15 (for preamble format 4: 0 to 6)
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:ZCZConfig?')
		return Conversions.str_to_int(response)

	def set_zcz_config(self, zero_corr_zone_con: int) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:ZCZConfig \n
		Snippet: driver.configure.prach.modulation.set_zcz_config(zero_corr_zone_con = 1) \n
		Specifies the zero correlation zone config, i.e. which NCS value of an NCS set is used for generation of the preamble
		sequence. For the combined signal path scenario, use CONFigure:LTE:SIGN<i>:CELL:PRACh:ZCZConfig. \n
			:param zero_corr_zone_con: numeric Range: 0 to 15 (for preamble format 4: 0 to 6)
		"""
		param = Conversions.decimal_value_to_str(zero_corr_zone_con)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:ZCZConfig {param}')

	# noinspection PyTypeChecker
	def get_ew_position(self) -> enums.LowHigh:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWPosition \n
		Snippet: value: enums.LowHigh = driver.configure.prach.modulation.get_ew_position() \n
		Specifies the position of the EVM window used for calculation of the trace results. \n
			:return: evm_window_pos: LOW | HIGH
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWPosition?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_ew_position(self, evm_window_pos: enums.LowHigh) -> None:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWPosition \n
		Snippet: driver.configure.prach.modulation.set_ew_position(evm_window_pos = enums.LowHigh.HIGH) \n
		Specifies the position of the EVM window used for calculation of the trace results. \n
			:param evm_window_pos: LOW | HIGH
		"""
		param = Conversions.enum_scalar_to_str(evm_window_pos, enums.LowHigh)
		self._core.io.write(f'CONFigure:LTE:MEASurement<Instance>:PRACh:MODulation:EWPosition {param}')

	def clone(self) -> 'ModulationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModulationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
