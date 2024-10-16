"""
    QuaO Project dwave_hybrid_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ..device.dwave_device import DwaveDevice
from ...data.device.circuit_running_option import CircuitRunningOption
from ...config.logging_config import *


class DwaveHybridDevice(DwaveDevice):

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug("[Dwave System] Create job")

        return self.device.sample_bqm(circuit, time_limit=10)

    def _get_provider_job_id(self, job) -> str:
        logger.debug("[Dwave System] Get provider job id")

        return job.id

    def _get_job_result(self, job):
        logger.debug('[Dwave System] Get job result')

        return job.result().get('sampleset')

    def _calculate_execution_time(self, job_result) -> float:
        logger.debug("[Dwave System] Calculate execution time")

        self.execution_time = (
            job_result.get("_info").get('run_time') / 1000
        )

        logger.debug(
            "[Dwave System] Execution time calculation was: {0} seconds".format(
                self.execution_time
            )
        )