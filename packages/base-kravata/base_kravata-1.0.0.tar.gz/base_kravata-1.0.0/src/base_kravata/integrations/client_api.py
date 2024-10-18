import json
import uuid
import os

from base_kravata.integrations.models.client_schema import ClientSchema
from .base_integration import BaseIntegrationApi
from .models import UserSchema


class ClientIntegrationApi(BaseIntegrationApi):

    def __init__(self):
        self._url = os.getenv("API_WCLIENT")

    def get_basic_data(self, user_id: uuid.UUID) -> ClientSchema:
        req = {"user_id": str(user_id)}
        res = self._post("/api/client/read", json.dumps(req))
        return ClientSchema().load(res)
