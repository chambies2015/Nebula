import importlib
import sys
import types
import unittest


class FakeCommand:
    def __init__(self, name, help_text=None, aliases=None):
        self.name = name
        self.help = help_text
        self.aliases = aliases or []


class FakeGroup(FakeCommand):
    def __init__(self, name, help_text=None):
        super().__init__(name, help_text)
        self.commands = []

    def command(self, name, help=None, aliases=None):
        def decorator(func):
            command = FakeCommand(name, help, aliases)
            self.commands.append(command)
            return command

        return decorator


def install_dependency_stubs():
    discord = types.ModuleType("discord")
    discord.Embed = object
    discord.Color = types.SimpleNamespace(blue=lambda: None)
    sys.modules["discord"] = discord

    discord_ext = types.ModuleType("discord.ext")
    discord_commands = types.ModuleType("discord.ext.commands")

    def group(name, help=None, invoke_without_command=False):
        def decorator(_func):
            return FakeGroup(name, help)

        return decorator

    discord_commands.group = group
    discord_commands.cooldown = lambda *_args, **_kwargs: lambda func: func
    discord_commands.BucketType = types.SimpleNamespace(user=object())
    discord_commands.Context = object
    discord_commands.Group = FakeGroup
    discord_ext.commands = discord_commands
    sys.modules["discord.ext"] = discord_ext
    sys.modules["discord.ext.commands"] = discord_commands

    aiohttp = types.ModuleType("aiohttp")
    aiohttp.ClientSession = object
    aiohttp.ClientResponse = object
    sys.modules["aiohttp"] = aiohttp

    ampapi_package = types.ModuleType("ampapi")
    ampapi_module = types.ModuleType("ampapi.ampapi")
    ampapi_module.AMPAPI = lambda _base_url: types.SimpleNamespace(sessionId=None)
    sys.modules["ampapi"] = ampapi_package
    sys.modules["ampapi.ampapi"] = ampapi_module


class CommandRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        install_dependency_stubs()
        sys.modules.pop("commands", None)
        cls.game_commands = importlib.import_module("commands")
        cls.config = importlib.import_module("config")

    def test_every_game_config_gets_a_command_group(self):
        self.assertEqual(
            set(self.config.GAME_CONFIGS),
            set(self.game_commands.GAME_COMMANDS),
        )

    def test_game_commands_remain_available_as_module_attributes(self):
        self.assertIs(
            self.game_commands.palworld,
            self.game_commands.GAME_COMMANDS["palworld"],
        )

    def test_batch_configs_do_not_need_instance_ids(self):
        batch_config = {"use_amp": False, "batch_script_path": "C:\\Server\\start.bat"}

        self.assertFalse(self.game_commands.uses_amp(batch_config))

    def test_palworld_is_batch_managed_with_restart_safe_process_matches(self):
        palworld_config = self.config.GAME_CONFIGS["palworld"]

        self.assertFalse(self.game_commands.uses_amp(palworld_config))
        self.assertFalse(palworld_config["keep_console_open"])
        self.assertIn("palserver.exe", palworld_config["process_match_terms"])
        self.assertIn("palserver-win64-shipping.exe", palworld_config["process_match_terms"])

    def test_palworld_info_config_includes_required_workshop_mods(self):
        info = self.config.GAME_CONFIGS["palworld"]["info"]

        self.assertIn("3625223587", info["mod_list"])
        self.assertIn("3625280368", info["mod_list"])
        self.assertIn("3762782874", info["mod_list"])
        self.assertNotIn("mod_package_path", info)

    def test_atm10_keeps_forcekill_command_by_default(self):
        command_names = {command.name for command in self.game_commands.atm10.commands}

        self.assertIn("forcekill", command_names)


if __name__ == "__main__":
    unittest.main()
