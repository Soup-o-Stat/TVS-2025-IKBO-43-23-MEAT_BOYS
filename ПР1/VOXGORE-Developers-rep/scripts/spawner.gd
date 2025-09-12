extends MeshInstance3D

var timer: int = 1000
var anim_playing=false

func _process(delta):
	if WaveHandler.start_wave and Global.enemies_on_arena<20:
		timer-=100*delta*WaveHandler.wave/2
		if timer<=0:
			var we_need_to_spawn=randi()%2
			if we_need_to_spawn==0 and anim_playing==false:
				$AnimationPlayer.play("spawn")
				anim_playing=true
			timer=1000-Global.enemy_kills*WaveHandler.wave*20
			if timer<200:
				timer=200

func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	if anim_name=="spawn":
		var enemy = preload("res://scenes/bloodsucker_1.tscn").instantiate()
		enemy.global_transform = $Marker3D.global_transform
		get_parent().add_child(enemy)
		Global.enemies_on_arena+=1
		anim_playing=false
