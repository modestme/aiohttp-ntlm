# aiohttp-ntlm

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NTLM authentication middleware for [aiohttp](https://github.com/aio-libs/aiohttp) (client support middleware since v3.12.0).

## Installation

Using pip:

```bash
pip install aiohttp-ntlm
```

## Usage Example

```python
import asyncio
import aiohttp
from aiohttp_ntlm import HttpNtlmAuthMiddleware

async def test_ntlm_auth_middleware() -> None:
    request_url: str = "<your_request_url>" 
    user_name: str = "<your_user_name>"
    password: str = "<your_password>"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                request_url, 
                headers={}, 
                middlewares=[HttpNtlmAuthMiddleware(user_name, password)]
            ) as response:
                if response.status == 200:
                    print("success：", await response.text())
        except Exception as e:
            raise Exception("error: " + str(e)) from e

if __name__ == "__main__":
    asyncio.run(test_ntlm_auth_middleware())
```

## Requirements

- Python >= 3.11
- aiohttp >= 3.12.13
- pyspnego >= 0.11.2

## Implementation Notes

This middleware is inspired by [requests_ntlm](https://github.com/requests/requests-ntlm) and implemented for aiohttp.