class AMPAPIError(Exception):
    pass


class AuthenticationError(AMPAPIError):
    pass


class InstanceNotFoundError(AMPAPIError):
    pass


class ServerStartError(AMPAPIError):
    pass


class ServerStopError(AMPAPIError):
    pass
