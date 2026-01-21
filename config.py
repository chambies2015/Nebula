ALLOWED_CHANNELS = ["1014955844913332334", "939660290172268583", "809544965386272790"]

AMP_BASE_URL = "http://localhost:8080/"
AMP_API_BASE = f"{AMP_BASE_URL}API"

URL_LOGIN = f"{AMP_API_BASE}/Core/Login"
URL_START = f"{AMP_API_BASE}/ADSModule/StartInstance"
URL_STOP = f"{AMP_API_BASE}/ADSModule/StopInstance"
URL_RESTART = f"{AMP_API_BASE}/ADSModule/RestartInstance"
URL_NETWORK_INFO = f"{AMP_API_BASE}/ADSModule/GetInstanceNetworkInfo"
URL_INSTANCES_STATUS = f"{AMP_API_BASE}/ADSModule/GetInstanceStatuses"
URL_GET_INSTANCE = f"{AMP_API_BASE}/ADSModule/GetInstance"

GAME_CONFIGS = {
    "ark": {
        "instance_id": "2033ec8f-244f-4af2-a568-4fb362448491",
        "instance_name": "ARKSurvivalEvolved01",
        "group_help": "ARK commands to start, stop, restart, and get info on the server",
        "embed_title": "Ark Bot Commands",
        "info": {
            "help": "Displays the server info for Ark Survival Evolved game server.",
            "embed_title": "ARK Survival Evolved Server Details",
            "ip": "67.4.158.45",
            "port": "7777",
            "name": "Chambies Private Server",
            "password": "thebois",
            "status_template": 'The Ark server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Ark Survival Evolved. Takes awhile due to large game.",
            "success_msg": "Successfully started spooling up the Ark server! This will take some time, ~15-20 minutes."
        },
        "stop": {
            "help": "Sends a stop signal to the Ark Survival Evolved game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Ark Survival Evolved game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "terraria": {
        "instance_id": "d5275053-eafc-493e-bbba-a5658231b7fe",
        "instance_name": "tModLoader1401",
        "group_help": "Terraria commands to start, stop, restart, and get info on the server",
        "embed_title": "Terraria Bot Commands",
        "info": {
            "help": "Displays the server info for the Terraria game server.",
            "embed_title": "Terraria Server Details",
            "ip": "67.4.158.45",
            "port": "7779",
            "password": "thebois",
            "mod_list": """
            Boss Checklist v1.4.0
            Calamity Mod v2.0.2.3
            Calamity Mod Music v2.0.2.2
            Calamity's Vanities v10.2
            Quality of Life 更好的体验 v1.6.3.3
            Magic Storage v0.5.7.10
            Max Stack Plus Extra v1.4.0.2
            Ore Excavator v0.8.4
            Recipe Browser v0.9.8
            """,
            "status_template": 'The Terraria server is currently {"running" if running_status else "not running or unable to get status"}.'
        },
        "start": {
            "help": "Starts up the Terraria game server relatively quick.",
            "success_msg": "Successfully started the terraria server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Terraria game server.",
            "success_msg": "Successfully stopped the terraria server!"
        },
        "restart": {
            "help": "Sends a restart signal to the Terraria game server.",
            "success_msg": "Successfully restarted the terraria server!"
        }
    },
    "necesse": {
        "instance_id": "592aa884-68c2-47ff-aaeb-cab0be49b395",
        "instance_name": "Necesse01",
        "group_help": "Necesse commands to start, stop, restart, and get info on the server",
        "embed_title": "Necesse Bot Commands",
        "info": {
            "help": "Displays the server info for the Necesse game server.",
            "embed_title": "Necesse Server Details",
            "ip": "67.4.158.45",
            "port": "15000",
            "password": "thebois",
            "status_template": 'The Necesse server is currently {"running" if running_status else "not running or unable to get status"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Necesse.",
            "success_msg": "Successfully started spooling up the Necesse server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Necesse game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Necesse game server, may take awhile.",
            "success_msg": "Successfully sent the restart signal to the server! This will take awhile and may fail..."
        }
    },
    "icarus": {
        "instance_id": "25bb4b25-053e-4992-b69f-3ac20ab5b105",
        "instance_name": "Icarus01",
        "group_help": "Icarus commands to start, stop, restart, and get info on the server",
        "embed_title": "Icarus Bot Commands",
        "info": {
            "help": "Displays the server info for the Icarus game server.",
            "embed_title": "Icarus Server Details",
            "ip": "67.4.158.45",
            "port": "19132",
            "name": "chambies private server",
            "password": "thebois",
            "status_template": 'The Icarus server is currently {"running" if running_status else "not running or unable to get status"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Icarus.",
            "success_msg": "Successfully started spooling up the Icarus server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Icarus game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Icarus game server, may take awhile.",
            "success_msg": "Successfully sent the restart signal to the server! This will take awhile and may fail..."
        }
    },
    "minecraft": {
        "instance_id": "123ffacd-896d-49db-b35a-14e76d13042a",
        "instance_name": "Minecraft01",
        "group_help": "Vanilla Minecraft commands to start, stop, restart, and get info on the server",
        "embed_title": "Vanilla Minecraft Bot Commands",
        "info": {
            "help": "Displays the server info for Vanilla Minecraft game server.",
            "embed_title": "Vanilla Minecraft Server Details",
            "ip": "67.4.158.45",
            "port": "25565",
            "name": "The Bois Server",
            "status_template": 'The Vanilla Minecraft server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Vanilla Minecraft.",
            "success_msg": "Successfully started spooling up the Vanilla Minecraft server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Vanilla Minecraft game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Vanilla Minecraft game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "satisfactory": {
        "instance_id": "ba176a72-d8f7-4bfc-b59d-52a4e7814612",
        "instance_name": "Satisfactory01",
        "group_help": "Satisfactory commands to start, stop, restart, and get info on the server",
        "embed_title": "Satisfactory Bot Commands",
        "info": {
            "help": "Displays the server info for Satisfactory game server.",
            "embed_title": "Satisfactory Server Details (NOT EXPERIMENTAL)",
            "ip": "67.4.158.45",
            "port": "7780",
            "status_template": 'The Satisfactory server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Satisfactory.",
            "success_msg": "Successfully started spooling up the Satisfactory server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Satisfactory game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Satisfactory game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "sevendaystodie": {
        "instance_id": "c1e805b3-d386-4de8-80e1-fae15cf1c589",
        "instance_name": "SevenDaysToDie01",
        "group_help": "Seven Days To Die commands to start, stop, restart, and get info on the server",
        "embed_title": "Seven Days To Die Bot Commands",
        "info": {
            "help": "Displays the server info for Seven Days To Die game server.",
            "embed_title": "Seven Days To Die Server Details",
            "ip": "67.4.158.45",
            "port": "27017",
            "name": "The Bois Server",
            "password": "thebois",
            "status_template": 'The Seven Days To Die server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Seven Days To Die.",
            "success_msg": "Successfully started spooling up the Seven Days To Die server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Seven Days To Die game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Seven Days To Die game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "projectzomboid": {
        "instance_id": "1c89f2a2-2586-46d2-945b-301cad9b6e08",
        "instance_name": "ProjectZomboid01",
        "group_help": "Project Zomboid commands to start, stop, restart, and get info on the server",
        "embed_title": "Project Zomboid Bot Commands",
        "info": {
            "help": "Displays the server info for Project Zomboid game server.",
            "embed_title": "Project Zomboid Server Details",
            "ip": "67.4.158.45",
            "port": "19133",
            "name": "The Bois Server",
            "password": "cumbo",
            "status_template": 'The Project Zomboid server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Project Zomboid.",
            "success_msg": "Successfully started spooling up the Project Zomboid server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Project Zomboid game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Project Zomboid game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "beamng": {
        "instance_id": "56309d72-174f-4fd6-bd29-75cdd0e3ef4e",
        "instance_name": "BeamMP01",
        "group_help": "BeamNG commands to start, stop, restart, and get info on the server",
        "embed_title": "BeamNG Bot Commands",
        "info": {
            "help": "Displays the server info for BeamNG game server.",
            "embed_title": "BeamNG Server Details",
            "ip": "67.4.161.61",
            "port": "34197",
            "status_template": 'The BeamNG server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for BeamNG.",
            "success_msg": "Successfully started spooling up the BeamNG server!"
        },
        "stop": {
            "help": "Sends a stop signal to the BeamNG game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the BeamNG game server, may take awhile.",
            "success_msg": "Successfully restarted the server! This will take awhile and may fail..."
        }
    },
    "sotf": {
        "instance_id": "6c7417c4-34d0-45d0-abc1-37ce4ad43009",
        "instance_name": "SonsOfTheForest01",
        "group_help": "Sons Of The Forest commands to start, stop, restart, and get info on the server",
        "embed_title": "Sons Of The Forest Bot Commands",
        "info": {
            "help": "Displays the server info for Sons Of The Forest game server.",
            "embed_title": "Sons Of The Forest Server Details",
            "ip": "67.4.161.61",
            "port": "37766",
            "status_template": 'The Sons Of The Forest server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Sons Of The Forest.",
            "success_msg": "Successfully started spooling up the Sons Of The Forest server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Sons Of The Forest game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Sons Of The Forest game server, may take awhile.",
            "success_msg": "Successfully sent a restart signal to the server! This will take awhile and may fail..."
        }
    },
    "enshrouded": {
        "instance_id": "d8019f76-cd48-4781-9b84-12506b14022c",
        "instance_name": "Enshrouded01",
        "group_help": "Enshrouded commands to start, stop, restart, and get info on the server",
        "embed_title": "Enshrouded Commands",
        "info": {
            "help": "Displays the server info for Enshrouded game server.",
            "embed_title": "Enshrouded Details",
            "ip": "67.4.161.61",
            "port": "15637",
            "status_template": 'The Enshrouded server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Enshrouded.",
            "success_msg": "Successfully started spooling up the Enshrouded server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Enshrouded game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Enshrouded game server, may take awhile.",
            "success_msg": "Successfully sent a restart signal to the server! This will take awhile and may fail..."
        }
    },
    "palworld": {
        "instance_id": "7e948276-2b9a-44fc-a40a-88db2e3d25b0",
        "instance_name": "Palworld01",
        "group_help": "Palworld commands to start, stop, restart, and get info on the server",
        "embed_title": "Palworld Commands",
        "info": {
            "help": "Displays the server info for Palworld game server.",
            "embed_title": "Palworld Details",
            "ip": "67.4.161.61",
            "port": "8211",
            "password": "beans",
            "status_template": 'The Palworld server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the spooling up process for Palworld.",
            "success_msg": "Successfully started spooling up the Palworld server!"
        },
        "stop": {
            "help": "Sends a stop signal to the Palworld game server.",
            "success_msg": "Successfully sent a stop signal to the server! Give it time to stop completely."
        },
        "restart": {
            "help": "Sends a restart signal to the Palworld game server, may take awhile.",
            "success_msg": "Successfully sent a restart signal to the server! This will take awhile and may fail..."
        }
    },
    "atm10": {
        "batch_script_path": "C:\\ATM10\\startserver.bat",
        "group_help": "ATM10 Minecraft server commands",
        "embed_title": "ATM10 Bot Commands",
        "info": {
            "help": "Displays the server info for the ATM10 Minecraft server.",
            "embed_title": "ATM10 Server Details",
            "ip": "67.4.161.61",
            "port": "25566",
            "status_template": 'The ATM10 server is currently {"running" if running_status else "not running"}.'
        },
        "start": {
            "help": "Starts the ATM10 Minecraft server using batch script.",
            "success_msg": "Successfully started the ATM10 server!"
        },
        "stop": {
            "help": "Stops the ATM10 Minecraft server gracefully.",
            "success_msg": "Successfully stopped the ATM10 server!"
        },
        "restart": {
            "help": "Restarts the ATM10 Minecraft server.",
            "success_msg": "Successfully restarted the ATM10 server!"
        }
    }
}
