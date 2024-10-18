class DBErrorWithRollback(Exception):
    code = "IN:001"


class InvalidModel(Exception):
    code = "IN:002"

class InvalidRequest(Exception):
    code = "IN:003"

class FailingExternalService(Exception):
    code = "IN:004"

class FailingExternalUserService(FailingExternalService):
    code = "IN:004:User"

class FailingExternalExternalService(FailingExternalService):
    code = "IN:004:External"

class FailingCRUD(Exception):
    code = "IN:005"

class FailingPartnerService(Exception):
    code = "IN:006"