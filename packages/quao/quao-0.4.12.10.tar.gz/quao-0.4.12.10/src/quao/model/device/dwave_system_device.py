"""
    QuaO Project dwave_system_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ..device.dwave_device import DwaveDevice
from ...data.device.circuit_running_option import CircuitRunningOption
from ...config.logging_config import *


class DwaveSystemDevice(DwaveDevice):

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug("[Dwave System] Create job")

        return self.device.sample(circuit)
