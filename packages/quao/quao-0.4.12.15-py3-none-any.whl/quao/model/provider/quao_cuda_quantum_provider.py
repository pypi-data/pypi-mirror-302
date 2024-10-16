"""
    QuaO Project quao_qiskit_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

import cudaq

from ...config.logging_config import logger
from ...model.provider.quao_provider import QuaoProvider

MULTI_GPU_DEVICE = "nvidia-mgpu"


class QuaoCudaQuantumProvider(QuaoProvider):
    def get_backend(self, device_specification):
        logger.debug("[Quao CUDA Quantum] Get backend")

        if MULTI_GPU_DEVICE.__eq__(device_specification):
            return cudaq.set_target(device_specification, ngpus="4")

        return cudaq.set_target(device_specification)

    def collect_provider(self):
        return None

    @staticmethod
    def __map_aer_backend_name(backend):
        return backend.configuration().backend_name
