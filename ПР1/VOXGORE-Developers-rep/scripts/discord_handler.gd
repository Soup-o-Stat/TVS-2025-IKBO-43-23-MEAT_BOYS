extends Node

func _set_discord_activity():
	DiscordRPC.app_id = 1334169923026419802
	DiscordRPC.details = ""
	DiscordRPC.state = ""
	DiscordRPC.large_image = "icon"
	DiscordRPC.start_timestamp = int(Time.get_unix_time_from_system())
	DiscordRPC.refresh()

func _update_discord_activity(details, state):
	DiscordRPC.details = details
	DiscordRPC.state = state
	DiscordRPC.start_timestamp = int(Time.get_unix_time_from_system())
	DiscordRPC.refresh()
	
func _ready():
	_set_discord_activity()
