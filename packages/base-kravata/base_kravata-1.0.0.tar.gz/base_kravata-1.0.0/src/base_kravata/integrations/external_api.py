import json
import os
from .base_integration import BaseIntegrationApi
from .models import CryptoAccount


class ExternalIntegrationApi(BaseIntegrationApi):
    def __init__(self) -> None:
        self._url = os.getenv("API_EXTERNAL")

    def create_crypto_account(self, vault_name) -> CryptoAccount:
        req = {"vaultName": vault_name}
        res = self._post("/api/external/custodian/add", json.dumps(req))
        crypto_acc = CryptoAccount().load(res)
        return crypto_acc
