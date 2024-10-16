"""
    QuaO Project quao_cuda_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

import time
import cudaq
from cudaq import spin
import numpy as np
from ...data.device.circuit_running_option import CircuitRunningOption
from ...enum.status.job_status import JobStatus
from ...model.device.quao_device import QuaoDevice
from ...config.logging_config import logger

layer_count: int = 2
parameter_count: int = 2 * layer_count

# The problem Hamiltonian
hamiltonian = (
    0.5 * spin.z(0) * spin.z(1)
    + 0.5 * spin.z(1) * spin.z(2)
    + 0.5 * spin.z(0) * spin.z(3)
    + 0.5 * spin.z(2) * spin.z(3)
)

# Specify the optimizer and its initial parameters. Make it repeatable.
cudaq.set_random_seed(13)
optimizer = cudaq.optimizers.COBYLA()
np.random.seed(13)
optimizer.initial_parameters = np.random.uniform(
    -np.pi / 8.0, np.pi / 8.0, parameter_count
)


class QuaoCudaQuantumDevice(QuaoDevice):
    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug(
            "[Quao CUDA Quantum] Create job with {0} shots".format(options.shots)
        )

        start_time = time.time()

        # Pass the kernel, spin operator, and optimizer to `cudaq.vqe`.
        optimal_expectation, optimal_parameters = cudaq.vqe(
            kernel=circuit,
            spin_operator=hamiltonian,
            optimizer=optimizer,
            parameter_count=parameter_count,
        )

        job = cudaq.sample(circuit, optimal_parameters, shots_count=options.shots)

        self.execution_time = time.time() - start_time

        return job

    def _produce_histogram_data(self, job_result) -> dict | None:
        logger.debug("[Quao CUDA Quantum] Produce histogram")

        return None

    def _get_provider_job_id(self, job) -> str:
        logger.debug("[Quao CUDA Quantum] Get provider job id")

        import uuid

        return str(uuid.uuid4())

    def _get_job_status(self, job) -> str:
        logger.debug("[Quao CUDA Quantum] Get job status")

        return JobStatus.DONE.value

    def _get_job_result(self, job):
        logger.debug("[Quao CUDA Quantum] Get job result")

        return job
