import base64

import spnego
from aiohttp import ClientHandlerType, ClientRequest, ClientResponse


class HttpNtlmAuthMiddleware:
    def __init__(self, username: str, password: str, auth_type: str = "NTLM"):
        self.username: str = username
        self.password: str = password

        self.auth_type: str = auth_type
        self.auth_strip: str = self.auth_type + " "

    async def __call__(self, req: ClientRequest, handler: ClientHandlerType) -> ClientResponse:
        resp: ClientResponse = await handler(req)

        if resp.status == 401:
            spnego_options: spnego.NegotiateOptions = spnego.NegotiateOptions.use_ntlm
            target_hostname: str = req.headers["Host"]
            client: spnego.ContextProxy = spnego.client(
                self.username,
                self.password,
                protocol="ntlm",
                channel_bindings=None,
                hostname=target_hostname,
                service="http",
                options=spnego_options,
            )
            negotiate_message: str = base64.b64encode(client.step() or b"").decode()
            auth: str = f"NTLM {negotiate_message}"
            req.headers["Authorization"] = auth

            resp = await handler(req)

            # get the challenge
            auth_header_value: str = resp.headers["WWW-Authenticate"]

            val: bytes = base64.b64decode(auth_header_value[len(self.auth_strip) :].encode())
            authenticate_message: str = base64.b64encode(client.step(val) or b"").decode()
            auth = f"{self.auth_type} {authenticate_message}"
            req.headers["Authorization"] = auth
            resp = await handler(req)

        return resp
