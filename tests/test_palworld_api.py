import unittest

import palworld_api


class PalworldRestApiTests(unittest.TestCase):
    def test_requires_complete_credentials(self):
        self.assertFalse(palworld_api.is_configured(None))
        self.assertFalse(
            palworld_api.is_configured(
                {
                    "base_url": "http://127.0.0.1:8212/v1/api",
                    "username": "admin",
                    "password": "",
                }
            )
        )

    def test_accepts_complete_credentials(self):
        self.assertTrue(
            palworld_api.is_configured(
                {
                    "base_url": "http://127.0.0.1:8212/v1/api",
                    "username": "admin",
                    "password": "not-a-real-password",
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
