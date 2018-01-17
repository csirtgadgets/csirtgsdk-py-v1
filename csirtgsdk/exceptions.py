
class CsirtgsdkException(Exception):
    def __init__(self, msg='Unknown'):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg


class AuthError(CsirtgsdkException):
    def __init__(self, msg='Unauthorized'):
        self.msg = msg


class TimeoutError(CsirtgsdkException):
    def __init__(self, msg='Timeout'):
        self.msg = msg


class InvalidSearch(CsirtgsdkException):
    def __init__(self, msg='Invalid Search'):
        self.msg = msg


class NotFound(CsirtgsdkException):
    def __init__(self, msg='Not Found'):
        self.msg = msg


class SubmissionFailed(CsirtgsdkException):
    def __init__(self, msg='Submission Failed'):
        self.msg = msg


class RateLimitExceeded(CsirtgsdkException):
    def __init__(self, msg='Rate Limit Threshold Exceeded'):
        self.msg = msg


class SystemBusy(CsirtgsdkException):
    def __init__(self, msg='System appears busy at the moment'):
        self.msg = msg