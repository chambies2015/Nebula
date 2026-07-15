import asyncio
from unittest import mock
import unittest

import batch_server


class FakeProcess:
    pid = 12345
    stdin = None

    def __init__(self, exit_code=None):
        self.exit_code = exit_code

    def poll(self):
        return self.exit_code


class BatchServerTests(unittest.TestCase):
    def setUp(self):
        batch_server.processes.clear()

    def tearDown(self):
        batch_server.processes.clear()

    def run_async(self, coroutine):
        return asyncio.run(coroutine)

    def test_start_returns_failure_when_process_exits_immediately(self):
        fake_process = FakeProcess(exit_code=1)

        with mock.patch.object(batch_server.os, "name", "posix"):
            with mock.patch.object(batch_server.os.path, "exists", return_value=True):
                with mock.patch.object(batch_server.subprocess, "Popen", return_value=fake_process):
                    success, message = self.run_async(
                        batch_server.start_batch_server("atm10", "startserver.bat")
                    )

        self.assertFalse(success)
        self.assertIn("exited immediately", message)
        self.assertIsNone(batch_server.processes["atm10"])

    def test_is_server_running_uses_process_discovery_after_bot_restart(self):
        with mock.patch.object(batch_server.os, "name", "nt"):
            with mock.patch.object(batch_server, "_find_related_java_processes", return_value=[object()]):
                self.assertTrue(batch_server.is_server_running("atm10"))

    def test_is_related_java_process_matches_atm10(self):
        process_info = {
            "name": "java.exe",
            "cmdline": ["java.exe", "-jar", "C:\\ATM10\\server.jar"],
        }

        self.assertTrue(batch_server._is_related_java_process(process_info, "atm10"))

    def test_is_related_java_process_ignores_non_java_process(self):
        process_info = {
            "name": "cmd.exe",
            "cmdline": ["cmd.exe", "/k", "C:\\ATM10\\startserver.bat"],
        }

        self.assertFalse(batch_server._is_related_java_process(process_info, "atm10"))

    def test_is_related_process_matches_palworld_executable(self):
        process_info = {
            "name": "PalServer-Win64-Shipping.exe",
            "cmdline": ["PalServer-Win64-Shipping.exe", "-port=8211"],
        }

        self.assertTrue(
            batch_server._is_related_process(
                process_info,
                ("palserver.exe", "palserver-win64-shipping.exe"),
            )
        )

    def test_is_related_process_ignores_command_line_mentions(self):
        process_info = {
            "name": "python.exe",
            "cmdline": ["python", "-c", "start PalServer.exe"],
        }

        self.assertFalse(
            batch_server._is_related_process(
                process_info,
                ("palserver.exe", "palserver-win64-shipping.exe"),
            )
        )

    def test_status_uses_named_process_discovery_for_palworld(self):
        with mock.patch.object(batch_server.os, "name", "nt"):
            with mock.patch.object(batch_server, "_find_related_processes", return_value=[object()]):
                self.assertTrue(
                    batch_server.is_server_running(
                        "palworld",
                        ("palserver.exe", "palserver-win64-shipping.exe"),
                    )
                )


if __name__ == "__main__":
    unittest.main()
