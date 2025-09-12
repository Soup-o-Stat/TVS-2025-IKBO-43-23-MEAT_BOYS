extends Node

var wave=0
var start_wave=false
var need_kills=0

func start_wave_func():
	wave+=1
	need_kills=randi_range(5*wave, 2*5*wave)
	start_wave=true
	
func _process(delta: float) -> void:
	if Global.enemy_kills>=need_kills and start_wave==true:
		start_wave=false
		Global.enemy_kills=0
