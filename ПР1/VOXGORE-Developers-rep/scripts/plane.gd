extends Node3D

func _ready():
	DiscordHandler._update_discord_activity("Plains", str(Global.score))
