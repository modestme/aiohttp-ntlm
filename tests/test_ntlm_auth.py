import os

import aiohttp
import pytest

from aiohttp_ntlm import HttpNtlmAuthMiddleware


@pytest.mark.asyncio
async def test_ntlm_auth_middleware() -> None:
    # Read configuration from environment variables
    request_url: str = os.getenv("NTLM_REQUEST_URL", "")
    user_name: str = os.getenv("NTLM_USERNAME", "")
    password: str = os.getenv("NTLM_PASSWORD", "")

    # Verify if required environment variables exist
    if not all([request_url, user_name, password]):
        pytest.skip("Missing required environment variables: NTLM_REQUEST_URL, NTLM_USERNAME, NTLM_PASSWORD")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                request_url, headers={}, middlewares=[HttpNtlmAuthMiddleware(user_name, password)]
            ) as response:
                assert response.status == 200
        except Exception as e:
            raise Exception("Request failed with error: " + str(e)) from e
