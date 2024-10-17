from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelBwCls:
	"""ChannelBw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channelBw", core, parent)

	def get_aggregated(self) -> float:
		"""SCPI: CONFigure:LTE:MEASurement<Instance>:CAGGregation:CBANdwidth:AGGRegated \n
		Snippet: value: float = driver.configure.carrierAggregation.channelBw.get_aggregated() \n
		Queries the width of the aggregated channel bandwidth. \n
			:return: ch_bandwidth: float Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:LTE:MEASurement<Instance>:CAGGregation:CBANdwidth:AGGRegated?')
		return Conversions.str_to_float(response)
