"""
    QuaO Project dwave_system_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from dwave.system import DWaveSampler, AutoEmbeddingComposite
from dwave.cloud import Client

from ...enum.provider_tag import ProviderTag
from ...model.provider.provider import Provider
from ...config.logging_config import *

system_devices = ["Advantage_system4.1"]
hybrid_devices = ["hybrid_binary_quadratic_model_version2"]


class DwaveSystemProvider(Provider):

    def __init__(self, api_token, endpoint):
        super().__init__(ProviderTag.D_WAVE)
        self.api_token = api_token
        self.endpoint = endpoint

    def get_backend(self, device_specification: str):
        logger.debug("[Dwave system] Get backend")

        if device_specification in system_devices:
            provider = self.collect_provider()
            return AutoEmbeddingComposite(provider)

        if device_specification in hybrid_devices:
            client = Client(endpoint=self.endpoint, token=self.api_token)
            return client.get_solver(device_specification)

        raise Exception("Unsupported Dwave device: {0}".format(device_specification))

    def collect_provider(self):
        logger.debug("[Dwave system] Connect to provider")

        return DWaveSampler(endpoint=self.endpoint, token=self.api_token)
