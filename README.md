# Nebula

A Discord bot for managing locally hosted game servers through the AMP (Application Management Panel) API. Nebula provides a unified interface to control multiple game servers directly from Discord, allowing users to start, stop, restart, and query server information with simple commands.

## Features

- **Multi-Game Support**: Manage 12+ different game servers from a single Discord bot
- **AMP API Integration**: Seamless integration with AMP for server management
- **Batch Server Support**: Direct batch script execution for servers not managed by AMP
- **Channel Restrictions**: Commands restricted to authorized Discord channels
- **Rate Limiting**: Built-in cooldown system (3 commands per 60 seconds per user)
- **Status Monitoring**: Real-time server status checking and information display
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Logging**: Rotating file logs for debugging and monitoring

## Supported Games

- ARK: Survival Evolved
- Terraria (tModLoader)
- Necesse
- Icarus
- Minecraft (Vanilla)
- Satisfactory
- Seven Days to Die
- Project Zomboid
- BeamNG
- Sons of The Forest
- Enshrouded
- Palworld
- ATM10 (Minecraft modpack)

## Architecture

### Core Components

- **`main.py`**: Discord bot initialization, event handlers, and command registration
- **`commands.py`**: Dynamic command group generation for each game server
- **`amp_client.py`**: AMP API client with authentication and session management
- **`batch_server.py`**: Batch script execution and process management for non-AMP servers
- **`config.py`**: Centralized configuration for all game servers and settings
- **`logger.py`**: Logging setup with file rotation
- **`exceptions.py`**: Custom exception classes for error handling

### Key Features

- **Dynamic Command Generation**: Game commands are automatically generated from configuration
- **Session Management**: Automatic token refresh for AMP API authentication
- **Process Tracking**: Monitors batch server processes for status and graceful shutdown
- **Embed Responses**: Rich Discord embeds for server information display

## Setup

### Prerequisites

- Python 3.7+
- Discord Bot Token
- AMP instance running on `localhost:8080`
- Access to game server instances configured in AMP

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install discord.py aiohttp ampapi psutil
   ```
3. Create `tokens.py` with your credentials:
   ```python
   bot_token = "your_discord_bot_token"
   username = "your_amp_username"
   password = "your_amp_password"
   ```
4. Create `sensitive.py` with server information:
   ```python
   SERVER_IPS = {
       "ark": "your_server_ip",
       # ... other game IPs
   }
   SERVER_PASSWORDS = {
       "ark": "your_password",
       # ... other game passwords
   }
   AUTHORIZED_USER_ID = your_discord_user_id
   ```
5. Configure `config.py` with your game server instance IDs and names
6. Update `ALLOWED_CHANNELS` in `config.py` with your Discord channel IDs

### Running

```bash
python main.py
```

## Usage

### Command Format

```
$<game> <action>
```

### Available Actions

- `info` - Display server information (IP, port, status, password, etc.)
- `start` (alias: `s`) - Start the game server
- `stop` (alias: `st`) - Stop the game server
- `restart` (alias: `r`) - Restart the game server
- `forcekill` - Force kill all related processes (ATM10 only, authorized users only)

### Examples

```
$ark info
$terraria start
$minecraft stop
$palworld restart
$help
```

### Help Command

Use `$help` (or `$h`, `$commands`) to see all available games and commands.

## Configuration

### Game Configuration

Each game is configured in `config.py` under `GAME_CONFIGS` with:
- Instance ID (for AMP-managed servers)
- Instance name
- Server IP and port
- Server password (if applicable)
- Help text and success messages
- Custom status templates

### Settings

- `ALLOWED_CHANNELS`: Discord channel IDs where commands are allowed
- `START_DELAY_SECONDS`: Delay after starting a server before confirmation
- `COMMAND_COOLDOWN_RATE`: Number of commands allowed per cooldown period
- `COMMAND_COOLDOWN_PER`: Cooldown period in seconds
- `AMP_BASE_URL`: Base URL for AMP API (default: `http://localhost:8080/`)

## Project Structure

```
Nebula/
├── main.py              # Discord bot entry point
├── commands.py          # Game command definitions
├── amp_client.py        # AMP API client
├── batch_server.py      # Batch server management
├── config.py            # Configuration and game settings
├── logger.py            # Logging setup
├── exceptions.py         # Custom exceptions
├── tokens.py            # Bot and API credentials (not in repo)
├── sensitive.py         # Server IPs and passwords (not in repo)
└── README.md            # This file
```

## Security Notes

- `tokens.py` and `sensitive.py` are not tracked in git (see `.gitignore`)
- Commands are restricted to specific Discord channels
- Rate limiting prevents command spam
- Force kill commands require authorized user ID

## License

This project is for personal use. Ensure you have proper authorization before deploying.
