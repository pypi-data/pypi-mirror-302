class PartnerIntegrationApi:
    EXAMPLE_RESPONSE_GET_BASIC_USER_DATA = {
        "id": "0001",
        "cellphone": "987654321",
        "dni": "1001123456",
        "firstname": "Pepito",
        "surname": "Pérez"
    }

    def get_external_account(self):
        return {
            "id": "123",
            "client_id": "b28dc8b9-9766-4ae3-97dc-281985920256",
            "name": "Testname",
            "type": "fiat",
            "number": "34",
            "register_date": "(03-10-2024)",
            "status": "active",
        }

    def get_basic_user_data(self, user_id):
        res = self.EXAMPLE_RESPONSE_GET_BASIC_USER_DATA.copy()
        res["id"] = user_id
        return res
