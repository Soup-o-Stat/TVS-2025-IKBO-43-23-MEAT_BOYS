extends StaticBody3D

var state="off"

func _on_button_area_area_entered(area: Area3D) -> void:
	if area.name.substr(0, 16)=="damage_collision" and WaveHandler.start_wave==false and Global.enemies_on_arena<=0:
		$MeshInstance3D.mesh=load("res://media/models/arena_button/button_on.vox")
		Global.enemy_kills=0
		WaveHandler.start_wave_func()
		$Label.text="Wave: "+str(WaveHandler.wave)
		$Label/AnimationPlayer.play("appear")
		state="on"
		Global.score+=(WaveHandler.wave+1)
		$AudioStreamPlayer.play()
		
func _process(delta: float) -> void:
	if WaveHandler.start_wave==false:
		if state=="on":
			var something_spawn_chance=randi()%99
			if something_spawn_chance>=0 and something_spawn_chance<40:	
				var hp_kit = preload("res://scenes/hp_kit.tscn").instantiate()
				hp_kit.global_transform = $Marker3D.global_transform
				get_parent().add_child(hp_kit)
			if something_spawn_chance>=40 and something_spawn_chance<80:	
				var weapon_box = preload("res://scenes/weapon_box.tscn").instantiate()
				weapon_box.global_transform = $Marker3D.global_transform
				get_parent().add_child(weapon_box)
		state="off"
		$MeshInstance3D.mesh=load("res://media/models/arena_button/button_off.vox")
