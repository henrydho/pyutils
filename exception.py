"""Generic exceptions used by the application"""

class IPSecException(Exception):
    """IPSec Exception"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IKEAuthError(IPSecException):
    """IKE Authentication Error exception"""

    def __init__(self, child_sa, error):
        message = str(
                f"[IKE] Establishing CHILD_SA '{child_sa}' failed: {error}"
                )
        super().__init__(message)
        self.child_sa = child_sa
        self.error = error


class IKETimeoutError(IPSecException):
    """IKE Timeout Exception"""

    def __init__(self, child_sa, error):
        message = str(
                f"[IKE] Establishing CHILD_SA '{child_sa}' failed: {error}"
                )
        super().__init__(message)
        self.child_sa = child_sa
        self.error = error


class IKEProposalError(IPSecException):
    """IKE Proposal Error exception"""

    def __init__(self, child_sa, error):
        message = str(
                f"[IKE] Establishing CHILD_SA '{child_sa}' failed: {error}. "
                "Verify and ensure the IPsec Parameters of both phase-1/phase-2 "
                "are matched between the IPSec peers."
                )
        super().__init__(message)
        self.child_sa = child_sa
        self.error = error


class IKEIDirError(IPSecException):
    """IKE IDir mismatched error

    :example: IDir '172.24.22.4' does not match to 'site-a@test.com'
    """
    def __init__(self, child_sa, error):
        message = str(
                f"[IKE] Establishing CHILD_SA '{child_sa}' failed: {error}"
                )
        super().__init__(message)
        self.child_sa = child_sa
        self.error = error


class IKEUknownError(IPSecException):
    """IKE Unknown Error exception"""

    def __init__(self, child_sa, error):
        message = str(
                f"[IKE] Establishing CHILD_SA '{child_sa}' failed: Unknown IKE error\n"
                f'{error}'
                )
        super().__init__(message)
        self.child_sa = child_sa
        self.error = error
