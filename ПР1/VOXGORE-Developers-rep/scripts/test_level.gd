extends Node3D


func _ready():
	#Engine.max_fps=60
	DiscordHandler._update_discord_activity("test_level", "Debug")
