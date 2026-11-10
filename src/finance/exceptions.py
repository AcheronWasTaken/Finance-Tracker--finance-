class RuntimeException(Exception):
    pass

class APIException(Exception):
    pass

class SubscriptionExists(RuntimeException):
    pass

class SubscriptionNotFound(RuntimeException):
    pass

class FieldExists(APIException):
    pass

class AnswerExists(APIException):
    pass