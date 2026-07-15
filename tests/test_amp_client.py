import asyncio
import importlib
import sys
import types
import unittest


class FakeResponse:
    def __init__(self, status, body):
        self.status = status
        self._body = body

    async def text(self):
        return self._body


def install_dependency_stubs():
    aiohttp = types.ModuleType("aiohttp")
    aiohttp.ClientSession = object
    aiohttp.ClientResponse = object
    sys.modules.setdefault("aiohttp", aiohttp)

    discord = types.ModuleType("discord")
    discord.Embed = object
    discord.Color = types.SimpleNamespace(blue=lambda: None)
    sys.modules.setdefault("discord", discord)

    ampapi_package = types.ModuleType("ampapi")
    ampapi_module = types.ModuleType("ampapi.ampapi")

    class FakeAMPAPI:
        def __init__(self, _base_url):
            self.sessionId = None

        async def Core_GetStatusAsync(self):
            return {"Metrics": {"CPU Usage": {"Percent": 0}}}

    ampapi_module.AMPAPI = FakeAMPAPI
    sys.modules.setdefault("ampapi", ampapi_package)
    sys.modules.setdefault("ampapi.ampapi", ampapi_module)


class AMPActionSuccessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        install_dependency_stubs()
        cls.amp_client = importlib.import_module("amp_client")

    def run_async(self, coroutine):
        return asyncio.run(coroutine)

    def test_json_false_response_is_failure(self):
        response = FakeResponse(200, '{"success": false, "message": "already stopped"}')

        result = self.run_async(self.amp_client.amp_action_succeeded(response))

        self.assertFalse(result)

    def test_json_true_response_is_success(self):
        response = FakeResponse(200, '{"success": true}')

        result = self.run_async(self.amp_client.amp_action_succeeded(response))

        self.assertTrue(result)

    def test_non_200_response_is_failure(self):
        response = FakeResponse(500, '{"success": true}')

        result = self.run_async(self.amp_client.amp_action_succeeded(response))

        self.assertFalse(result)

    def test_empty_200_response_preserves_legacy_success_behavior(self):
        response = FakeResponse(200, "")

        result = self.run_async(self.amp_client.amp_action_succeeded(response))

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
