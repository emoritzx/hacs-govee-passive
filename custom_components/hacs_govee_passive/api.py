"""Govee API Client"""
import aiohttp
import async_timeout
import asyncio
import json
import jwt
import logging
import socket
import uuid
from datetime import datetime

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}

LOGIN_ENDPOINT = "https://app2.govee.com/account/rest/account/v1/login"
DEVICE_ENDPOINT = "https://app2.govee.com/device/rest/devices/v1/list"


class GoveeApiClient:
    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session
        self._token = None

    @property
    def token_expired(self) -> bool:
        if not self._token:
            return True
        raw_token = self._token
        token = jwt.decode(raw_token, options={"verify_signature": False})
        expiration_timestamp = token["exp"]
        expiration_time = datetime.fromtimestamp(expiration_timestamp)
        return expiration_time < datetime.now()

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        if self.token_expired:
            await self._do_login()
        headers = {"Authorization": f"Bearer {self._token}"}
        response = await self.api_wrapper(DEVICE_ENDPOINT, headers=headers)
        self._check_inner_status(response)
        return response["devices"]

    async def _do_login(self):
        data = {
            "email": self._username,
            "password": self._password,
            "client": str(uuid.uuid4()),
        }
        response = await self.api_wrapper(LOGIN_ENDPOINT, data=data, headers=HEADERS)
        self._check_inner_status(response)

        # save token
        client_data = response["client"]
        self._token = client_data["token"]

    def _check_inner_status(self, payload):
        # check data response code
        # I dunno why it's different than the HTTP response code 🙄
        inner_status_code = payload["status"]
        if inner_status_code != 200:
            raise Exception(
                f"Error logging in ({inner_status_code}): {payload['message']}"
            )

    async def api_wrapper(self, url: str, data: dict = {}, headers: dict = {}) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.post(url, headers=headers, json=data)
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)


class MockGoveeApiClient(GoveeApiClient):
    async def async_get_data(self) -> dict:
        with open(".vscode/mock_data.json", "r") as f:
            mock_data = json.load(f)
        return mock_data
