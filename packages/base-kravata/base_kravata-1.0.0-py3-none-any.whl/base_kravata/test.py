import unittest, uuid
from abc import abstractmethod
from werkzeug.test import TestResponse
from .config import app 

class TestSession:

    def commit(self):
        pass

    def rollback(self):
        pass

class TestBaseRepository:

    def __init__(self) -> None:
        self.session = TestSession()

    def save(self, obj):
        obj.id = uuid.uuid4()
        return obj

class TestBase(unittest.TestCase):

    @abstractmethod
    def _prepare_data(self): 
        pass

    @classmethod
    def setUpClass(self):
        try:
            self.client = app.test_client()
            self.base_url = "/api"
            self._prepare_data(self)
        except Exception as e:
            print(e.args)
            assert True == False


    def process_req(self, method:str, parameters = None, req = None, check_error = True) -> TestResponse:
        if parameters:
            for ele in parameters:
                self.base_url = self.base_url.replace(f":{ele}",parameters[ele])
				
		#test
        print(self.base_url)
        if method.lower() == "get":
            response = self.client.get(self.base_url)
        elif method.lower() == "post":
            response = self.client.post(self.base_url, json=req)
        elif method.lower() == "put":
            response = self.client.put(self.base_url, json=req)
        else:
            response = self.client.delete(self.base_url)
        assert response.status_code >= 200 < 230
        if isinstance(response.json, dict):
            if check_error:
                assert not "error" in response.json
        elif isinstance(response.json, bool) or isinstance(response.json, list):
            assert True
        else:
            assert False
        return response