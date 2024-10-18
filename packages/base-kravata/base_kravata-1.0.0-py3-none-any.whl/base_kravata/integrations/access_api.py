
import json
import uuid
import requests, os
from .base_integration import BaseIntegrationApi
from .models import UserSchema

class AccessIntegrationApi(BaseIntegrationApi):

    def __init__(self):
        self._url = os.getenv("API_ACCESS")

    def save_user(self, user : UserSchema) -> UserSchema:
        res = self._post(os.getenv("API_ACCESS_USER"), user.dump())
        res = UserSchema().load(res)
        return res
    
    def get_user(self, user_id : uuid.UUID) -> UserSchema:
        res = self._get(os.getenv("API_ACCESS_USER") + "/" + user_id)
        res = UserSchema().load(res)
        return res