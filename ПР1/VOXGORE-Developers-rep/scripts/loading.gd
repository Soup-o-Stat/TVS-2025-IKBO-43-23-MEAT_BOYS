extends Node2D

var tips=["Dont forget to reload your gun!"]

func _ready() -> void:
	PlayerData.hp= 3
	PlayerData.max_hp= 3
	PlayerData.max_speed= 10
	PlayerData.softlock=false
	
	Global.enemy_kills=0
	Global.score=0
	Global.enemies_on_arena=0
	
	WaveHandler.wave=0
	WaveHandler.start_wave=false
	WaveHandler.need_kills=0

func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	get_tree().change_scene_to_file("res://scenes/plane.tscn")
